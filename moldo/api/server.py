"""
server.py - FastAPI application for the Moldo backend.

Endpoints:
    GET  /health              → { status, timestamp }
    POST /run                 → { stdout, errors, highlights }
    WS   /ws/run              → real-time execution with highlight/input events
    GET  /molds               → { molds: [...manifests] }
    POST /molds/install       → { manifest }
    DELETE /molds/{name}      → { ok }
"""
import io
import json
import logging
import re
import tempfile
import traceback
import zipfile
from contextlib import asynccontextmanager, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from moldo.core.compiler import ProgramCompiler
from moldo.core.interpreter import MoldoInterpreter
from moldo.core.mold_registry import MoldRegistry

logger = logging.getLogger('moldo')

# Directory scanned on startup for pre-installed community molds
_WATCH_DIR = Path.home() / 'Downloads' / 'molds'


def _auto_install_molds(registry: MoldRegistry) -> None:
    """Scan _WATCH_DIR and install any .mold files not already registered."""
    if not _WATCH_DIR.exists():
        return
    for mold_file in sorted(_WATCH_DIR.glob('*.mold')):
        try:
            with zipfile.ZipFile(mold_file) as zf:
                if 'moldo.json' not in zf.namelist():
                    continue
                manifest = json.loads(zf.read('moldo.json'))
                mold_name = manifest.get('name', '')
            if not mold_name:
                continue
            if registry.get_mold(mold_name):
                logger.info('Mold "%s" already installed - skipping', mold_name)
                continue
            registry.install(mold_file)
            logger.info('Auto-installed mold "%s" from %s', mold_name, mold_file.name)
        except Exception as exc:
            logger.warning('Could not auto-install %s: %s', mold_file.name, exc)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _auto_install_molds(_registry)
    yield


app = FastAPI(title='Moldo Backend', version='0.5.0', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# Singleton registry + compiler - shared across all requests
_registry = MoldRegistry()
_compiler  = ProgramCompiler(registry=_registry)


# ── Models ────────────────────────────────────────────────────

class ProgramPayload(BaseModel):
    version: str = '1.0'
    molds:   list[str] = []
    program: dict


class RunResult(BaseModel):
    stdout:     list[str]
    errors:     list[str]
    highlights: list[str]


class HealthResponse(BaseModel):
    status:    str
    timestamp: str


# ── Routes ────────────────────────────────────────────────────

@app.get('/health', response_model=HealthResponse)
async def health():
    return HealthResponse(
        status='OK',
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post('/run', response_model=RunResult)
async def run_program(payload: ProgramPayload):
    """Compile and execute a JSON program tree."""
    try:
        source = _compiler.compile(payload.dict())
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f'Compile error: {exc}')

    stdout_lines: list[str] = []
    error_lines:  list[str] = []
    highlights:   list[str] = []

    # Collect node IDs from comments emitted by the compiler (# node-N)
    for line in source.splitlines():
        m = re.match(r'\s*#\s*(node-\S+)', line)
        if m:
            highlights.append(m.group(1))

    # Execute in an isolated namespace with stdout captured
    buf       = io.StringIO()
    namespace = {}
    try:
        with redirect_stdout(buf):
            exec(compile(source, '<moldo>', 'exec'), namespace)  # noqa: S102
    except Exception:
        tb = traceback.format_exc()
        user_lines = [l for l in tb.splitlines() if '<moldo>' in l or 'Error' in l]
        error_lines = user_lines or [tb.splitlines()[-1]]

    stdout_lines = [l for l in buf.getvalue().splitlines() if l]

    return RunResult(stdout=stdout_lines, errors=error_lines, highlights=highlights)


@app.get('/molds')
async def list_molds():
    return {'molds': _registry.all_molds()}


@app.post('/molds/install')
async def install_mold(file: UploadFile = File(...)):
    """Accept a .zip.mold upload, extract, pip-install deps, and register."""
    if not (file.filename or '').endswith('.mold'):
        raise HTTPException(status_code=400, detail='File must have a .mold extension')

    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = Path(tmp.name)

    try:
        manifest = _registry.install(tmp_path)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    finally:
        tmp_path.unlink(missing_ok=True)

    return {'manifest': manifest}


@app.delete('/molds/{mold_name}')
async def uninstall_mold(mold_name: str):
    if not _registry.get_mold(mold_name):
        raise HTTPException(status_code=404, detail=f'Mold "{mold_name}" not found')
    _registry.uninstall(mold_name)
    return {'ok': True}


# ── Real-time WebSocket execution ──────────────────────────────

@app.websocket('/ws/run')
async def ws_run(ws: WebSocket):
    """
    Real-time execution bridge.

    Client → server: { type: "start", protocol: {...} }
    Server → client: { type: "highlight", canvasId: "..." }
                     { type: "output",    value: "..." }
                     { type: "error",     message: "..." }
                     { type: "input_request", message: "...", dataType: "..." }
    Client → server: { type: "input_response", value: "..." }
    Server → client: { type: "done" }
    """
    await ws.accept()
    try:
        msg = await ws.receive_json()
        if msg.get('type') != 'start':
            await ws.send_json({'type': 'error', 'message': 'Expected type=start'})
            await ws.close()
            return

        program    = (msg.get('protocol') or {}).get('program')
        step_delay = float(msg.get('stepDelay') or 0)
        if not program:
            await ws.send_json({'type': 'error', 'message': 'No program in protocol'})
            await ws.close()
            return

        async def send(event: dict) -> None:
            await ws.send_json(event)

        async def recv() -> dict:
            return await ws.receive_json()

        interpreter = MoldoInterpreter(registry=_registry)
        try:
            await interpreter.run(program, send, recv, step_delay=step_delay)
        except Exception as exc:
            await ws.send_json({'type': 'error', 'message': str(exc)})

        await ws.send_json({'type': 'done'})

    except WebSocketDisconnect:
        pass
    except Exception as exc:
        logger.warning('ws_run error: %s', exc)
        try:
            await ws.send_json({'type': 'error', 'message': str(exc)})
        except Exception:
            pass
