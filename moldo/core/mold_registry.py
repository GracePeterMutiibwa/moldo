"""
mold_registry.py - loads, stores, and queries installed molds.

Built-in molds live in moldo/molds/<name>/ and are always present.
Community molds are installed into moldo/installed/<name>/ at runtime.

Public API:
    registry = MoldRegistry()
    registry.get_block('math', 'sqrt')  → block manifest dict | None
    registry.get_mold('math')           → mold manifest dict  | None
    registry.all_molds()                → list of manifest dicts
    registry.install(zip_path)          → manifest dict  (extracts + registers)
    registry.uninstall(mold_name)       → None
"""
import importlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

# Paths
_PACKAGE_DIR   = Path(__file__).parent.parent          # moldo/
_BUILTIN_DIR   = _PACKAGE_DIR / 'molds'               # moldo/molds/
_INSTALLED_DIR = _PACKAGE_DIR / 'installed'            # moldo/installed/


class MoldRegistry:
    def __init__(self):
        self._molds: dict[str, dict] = {}   # name → manifest
        self._blocks: dict[str, dict] = {}  # "name.blockId" → block entry

        _INSTALLED_DIR.mkdir(exist_ok=True)
        self._load_all_builtins()
        self._load_all_installed()

    # ── Queries ────────────────────────────────────────────────

    def get_mold(self, name: str) -> dict | None:
        return self._molds.get(name)

    def get_block(self, mold_name: str, block_id: str) -> dict | None:
        return self._blocks.get(f'{mold_name}.{block_id}')

    def all_molds(self) -> list[dict]:
        return list(self._molds.values())

    # ── Install / uninstall ────────────────────────────────────

    def install(self, zip_path: Path) -> dict:
        """
        Extract a .zip.mold file, validate its moldo.json, pip-install
        requirements.txt, and register it. Returns the manifest.
        """
        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
            if 'moldo.json' not in names:
                raise ValueError('moldo.json not found in the mold archive')

            manifest = json.loads(zf.read('moldo.json'))
            mold_name = manifest.get('name')
            if not mold_name:
                raise ValueError('moldo.json must have a "name" field')

            dest = _INSTALLED_DIR / mold_name
            if dest.exists():
                shutil.rmtree(dest)
            zf.extractall(dest)

        # Install pip dependencies if requirements.txt exists
        req_file = dest / 'requirements.txt'
        if req_file.exists():
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', '-r', str(req_file)],
                stdout=subprocess.DEVNULL,
            )

        # Add the mold package to sys.path so imports work
        if str(dest) not in sys.path:
            sys.path.insert(0, str(dest))

        self._register(manifest, mold_dir=dest)
        return manifest

    def uninstall(self, mold_name: str) -> None:
        dest = _INSTALLED_DIR / mold_name
        if dest.exists():
            shutil.rmtree(dest)
        self._deregister(mold_name)

    # ── Internal loading ───────────────────────────────────────

    def _load_all_builtins(self):
        for mold_dir in _BUILTIN_DIR.iterdir():
            manifest_path = mold_dir / 'moldo.json'
            if manifest_path.exists():
                manifest = json.loads(manifest_path.read_text())
                self._register(manifest, mold_dir=mold_dir)

    def _load_all_installed(self):
        for mold_dir in _INSTALLED_DIR.iterdir():
            manifest_path = mold_dir / 'moldo.json'
            if manifest_path.exists():
                manifest = json.loads(manifest_path.read_text())
                if str(mold_dir) not in sys.path:
                    sys.path.insert(0, str(mold_dir))
                self._register(manifest, mold_dir=mold_dir)

    def _register(self, manifest: dict, mold_dir: Path = None):
        name = manifest['name']
        manifest['_dir'] = str(mold_dir) if mold_dir else None
        self._molds[name] = manifest

        for block in manifest.get('blocks', []):
            key = f'{name}.{block["id"]}'
            self._blocks[key] = {**block, 'moldName': name}

    def _deregister(self, name: str):
        mold = self._molds.pop(name, None)
        if not mold:
            return
        for block in mold.get('blocks', []):
            self._blocks.pop(f'{name}.{block["id"]}', None)

    def resolve_callable(self, mold_name: str, python_call: str):
        """
        Import and return the Python callable named in pythonCall.
        e.g. "webscraper.fetch_page" → webscraper module's fetch_page function.
        Raises ImportError / AttributeError if not found.
        """
        parts  = python_call.rsplit('.', 1)
        module = importlib.import_module(parts[0])
        return getattr(module, parts[1])
