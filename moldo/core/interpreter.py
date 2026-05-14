"""
interpreter.py - Real-time tree-walking interpreter for the Moldo JSON protocol.

Walks the program tree node-by-node, firing send() events (highlight, output,
input_request, error) and awaiting recv() responses (input_response) so the
frontend can animate execution in real time.
"""

import asyncio
import importlib
import math as _math
import operator
from typing import Any, Awaitable, Callable

Send = Callable[[dict], Awaitable[None]]
Recv = Callable[[], Awaitable[dict]]

_BINARY_OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "//": operator.floordiv,
    "**": operator.pow,
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
}
_MODIFY_OPS = {
    "+=": operator.add,
    "-=": operator.sub,
    "*=": operator.mul,
    "/=": operator.truediv,
    "%=": operator.mod,
}


def _resolve(value: Any, ns: dict) -> Any:
    if not isinstance(value, str):
        return value
    # Variable reference
    if value.startswith("@"):
        return ns.get(value[1:])
    # Python literals
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() == "none":
        return None
    # f-string: f"...{var}..."
    if len(value) >= 3 and value.startswith('f"') and value.endswith('"'):
        inner, out, i = value[2:-1], "", 0
        while i < len(inner):
            if inner[i] == "{":
                j = inner.find("}", i)
                if j == -1:
                    out += inner[i]
                    i += 1
                else:
                    out += str(ns.get(inner[i + 1 : j], ""))
                    i = j + 1
            else:
                out += inner[i]
                i += 1
        return out
    # Quoted string literal
    if len(value) >= 2 and value[0] in ('"', "'") and value[-1] == value[0]:
        return value[1:-1]
    # Numeric
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def _cast(value: Any, dtype: str) -> Any:
    dtype = (dtype or "text").lower()
    if dtype == "int":
        return int(float(str(value)))
    if dtype == "float":
        return float(str(value))
    if dtype == "bool":
        return bool(value)
    return str(value)


class MoldoInterpreter:
    def __init__(self, registry=None):
        self._registry = registry

    async def run(self, program: dict, send: Send, recv: Recv, step_delay: float = 0.0) -> None:
        self._step_delay = max(0.0, float(step_delay or 0))
        ns: dict = {}
        await self._walk(program, ns, send, recv)

    # Core walker ────────────────────

    async def _walk(self, node: dict | None, ns: dict, send: Send, recv: Recv) -> None:
        if not node:
            return

        mold = node.get("mold", "")
        block = node.get("block", "")
        params = node.get("params", {})
        canvas_id = node.get("canvasId")

        if canvas_id:
            await send({"type": "highlight", "canvasId": canvas_id})
            if self._step_delay > 0:
                await asyncio.sleep(self._step_delay)

        handled_next = False
        try:
            if mold == "variables":
                self._do_variables(block, params, ns)
            elif mold == "io":
                await self._do_io(block, params, ns, send, recv)
            elif mold == "control":
                await self._do_control(node, block, params, ns, send, recv)
                handled_next = True  # control manages its own continuation
            elif mold == "math":
                self._do_math(block, params, ns)
            elif mold == "text":
                self._do_text(block, params, ns)
            elif mold == "collections":
                self._do_collections(block, params, ns)
            else:
                await self._do_community(mold, block, params, ns, send)
        except Exception as exc:
            await send({"type": "error", "message": str(exc)})
            return

        if not handled_next:
            await self._walk(node.get("next"), ns, send, recv)

    # Variables ──────────────────────

    def _do_variables(self, block: str, params: dict, ns: dict) -> None:
        if block == "declare":
            ns[params["name"]] = _cast(
                _resolve(params.get("value", ""), ns),
                params.get("dataType", "text"),
            )
        elif block == "assign":
            ns[params["target"]] = _resolve(params["value"], ns)
        elif block == "modify":
            fn = _MODIFY_OPS.get(params.get("operator", "+="), operator.add)
            ns[params["target"]] = fn(
                ns.get(params["target"], 0),
                _resolve(params["value"], ns),
            )

    # IO ─────────────────────────────

    async def _do_io(self, block: str, params: dict, ns: dict, send: Send, recv: Recv) -> None:
        if block == "print":
            val = _resolve(params.get("value", ""), ns)
            await send({"type": "output", "value": str(val)})
        elif block == "prompt":
            msg = _resolve(params.get("message", '"Enter value:"'), ns)
            dtype = params.get("dataType", "text")
            target = params.get("target", "_inp")
            # Strip surrounding quotes from message if present
            msg_str = str(msg)
            if len(msg_str) >= 2 and msg_str[0] == '"' and msg_str[-1] == '"':
                msg_str = msg_str[1:-1]
            await send({"type": "input_request", "message": msg_str, "dataType": dtype})
            response = await recv()
            ns[target] = _cast(response.get("value", ""), dtype)

    # Control ────────────────────────

    async def _do_control(
        self, node: dict, block: str, params: dict, ns: dict, send: Send, recv: Recv
    ) -> None:
        if block == "branch":
            left = _resolve(params.get("left", ""), ns)
            right = _resolve(params.get("right", ""), ns)
            fn = _BINARY_OPS.get(params.get("operator", "=="), operator.eq)
            try:
                taken = fn(left, right)
            except Exception:
                taken = False
            branches = node.get("branches", {})
            chosen = branches.get("true") if taken else branches.get("false")
            await self._walk(chosen, ns, send, recv)
            await self._walk(node.get("next"), ns, send, recv)

        elif block == "forLoop":
            start = int(_resolve(params.get("from", "0"), ns) or 0)
            end = int(_resolve(params.get("to", "0"), ns) or 0)
            step = int(_resolve(params.get("step", "1"), ns) or 1)
            var = params.get("variable", "_i")
            body = node.get("body")
            for i in range(start, end, step or 1):
                ns[var] = i
                await self._walk(body, ns, send, recv)
            await self._walk(node.get("next"), ns, send, recv)

        elif block == "whileLoop":
            fn = _BINARY_OPS.get(params.get("operator", "<"), operator.lt)
            body = node.get("body")
            for _ in range(10_000):
                left = _resolve(params.get("left", ""), ns)
                right = _resolve(params.get("right", ""), ns)
                try:
                    if not fn(left, right):
                        break
                except Exception:
                    break
                await self._walk(body, ns, send, recv)
            await self._walk(node.get("next"), ns, send, recv)

    # Math ───────────────────────────

    def _do_math(self, block: str, params: dict, ns: dict) -> None:
        r = params.get("result", "_r")
        raw = params.get("value", params.get("left", 0))
        a = _resolve(raw, ns)
        b = _resolve(params.get("right", 0), ns)
        try:
            af, bf = float(a), float(b)
        except (TypeError, ValueError):
            af, bf = 0.0, 0.0
        if block == "arithmetic":
            ns[r] = _BINARY_OPS.get(params.get("operator", "+"), operator.add)(af, bf)
        elif block == "sqrt":
            ns[r] = _math.sqrt(af)
        elif block == "power":
            ns[r] = af**bf
        elif block == "round":
            ns[r] = round(af, int(bf))
        elif block == "abs":
            ns[r] = abs(af)
        elif block == "floor":
            ns[r] = _math.floor(af)
        elif block == "ceil":
            ns[r] = _math.ceil(af)

    # Text ───────────────────────────

    def _do_text(self, block: str, params: dict, ns: dict) -> None:
        r = params.get("result", "_r")
        val = str(_resolve(params.get("value", ""), ns))
        b = _resolve(params.get("other", params.get("separator", params.get("old", ""))), ns)
        if block == "upper":
            ns[r] = val.upper()
        elif block == "lower":
            ns[r] = val.lower()
        elif block == "length":
            ns[r] = len(val)
        elif block == "join":
            ns[r] = val + str(b)
        elif block == "split":
            ns[r] = val.split(str(b))
        elif block == "contains":
            ns[r] = str(b) in val
        elif block == "replace":
            new_val = str(_resolve(params.get("new", ""), ns))
            ns[r] = val.replace(str(b), new_val)

    # Collections ────────────────────

    def _do_collections(self, block: str, params: dict, ns: dict) -> None:
        r = params.get("result", "_r")
        if block == "createList":
            ns[r] = []
        elif block == "append":
            lst = _resolve(params.get("list", ""), ns)
            item = _resolve(params.get("item", ""), ns)
            if isinstance(lst, list):
                lst.append(item)
        elif block == "removeItem":
            lst = _resolve(params.get("list", ""), ns)
            idx = int(_resolve(params.get("index", 0), ns))
            if isinstance(lst, list) and 0 <= idx < len(lst):
                lst.pop(idx)
        elif block == "getItem":
            lst = _resolve(params.get("list", ""), ns)
            idx = int(_resolve(params.get("index", 0), ns))
            ns[r] = lst[idx] if isinstance(lst, list) and 0 <= idx < len(lst) else None
        elif block == "createDict":
            ns[r] = {}
        elif block == "getKey":
            d = _resolve(params.get("dict", ""), ns)
            key = str(_resolve(params.get("key", ""), ns))
            ns[r] = d.get(key) if isinstance(d, dict) else None
        elif block == "setKey":
            d = _resolve(params.get("dict", ""), ns)
            key = str(_resolve(params.get("key", ""), ns))
            val = _resolve(params.get("value", ""), ns)
            if isinstance(d, dict):
                d[key] = val

    # Community molds ────────────────

    async def _do_community(
        self, mold: str, block: str, params: dict, ns: dict, send: Send
    ) -> None:
        if not self._registry:
            return
        mold_manifest = self._registry.get_mold(mold)
        if not mold_manifest:
            await send({"type": "error", "message": f"Unknown mold: {mold}"})
            return
        block_def = next((b for b in mold_manifest.get("blocks", []) if b["id"] == block), None)
        if not block_def:
            await send({"type": "error", "message": f"Unknown block: {mold}.{block}"})
            return
        python_call = block_def.get("pythonCall", "")
        if not python_call:
            return

        module_name, fn_name = python_call.rsplit(".", 1)
        try:
            mod = importlib.import_module(module_name)
            fn = getattr(mod, fn_name)
        except Exception as exc:
            await send({"type": "error", "message": f"Import error: {exc}"})
            return

        output_ids = {o["id"] for o in block_def.get("outputs", [])}
        call_kwargs = {k: _resolve(v, ns) for k, v in params.items() if k not in output_ids}
        try:
            result = fn(**call_kwargs)
        except Exception as exc:
            await send({"type": "error", "message": f"{python_call}: {exc}"})
            return

        for out in block_def.get("outputs", []):
            var_name = str(params.get(out["id"], "")).strip()
            if var_name:
                ns[var_name] = result
