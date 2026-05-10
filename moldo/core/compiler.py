"""
compiler.py - walks a JSON program tree and produces executable Python source.

The program tree shape (from MoldoCompiler.js):
    {
      "version": "1.0",
      "molds":   ["variables", "io", ...],
      "program": {
        "id":     "node-1",
        "mold":   "variables",
        "block":  "declare",
        "params": { "name": "x", "value": "10", "dataType": "int" },
        "next":   { ... }          # linear next
        # OR
        "branches": { "true": {...}, "false": {...} }   # decision
        # OR
        "body": {...}, "next": {...}                     # loop / function define
      }
    }

param values prefixed with "@" are variable references (e.g. "@score").
The compiler strips the "@" and emits the bare name.
"""
from __future__ import annotations
import re


def _val(raw: str | None) -> str:
    """Resolve a param value: "@score" → "score", "42" → "42", "" → '""'."""
    if raw is None:
        return '""'
    s = str(raw).strip()
    if s.startswith('@'):
        return s[1:]           # variable reference
    if s == '':
        return '""'
    return s


def _str_val(raw: str | None) -> str:
    """
    Like _val but wraps plain literals in quotes so Python treats them as strings.
    Variable refs and things that already look like Python expressions are left alone.
    """
    if raw is None:
        return '""'
    s = str(raw).strip()
    if s.startswith('@'):
        return s[1:]
    if s == '':
        return '""'
    # If it's already quoted, a number, a bool literal, or an f-string, pass through
    if (s.startswith('"') or s.startswith("'") or s.startswith('f"') or s.startswith("f'")
            or re.match(r'^-?\d+(\.\d+)?$', s)
            or s in ('True', 'False', 'None')):
        return s
    return repr(s)   # wrap bare text in quotes


class ProgramCompiler:
    def __init__(self, registry=None):
        self._registry = registry   # MoldRegistry (optional, used for community molds)

    def compile(self, program: dict) -> str:
        """
        Top-level: turn the full program dict into a Python source string.
        """
        self._community_imports: set[str] = set()

        body: list[str] = []
        self._walk(program.get('program'), body, indent=0)

        header = ['import math as _math', 'import random as _random']
        for mod in sorted(self._community_imports):
            header.append(f'import {mod}')
        header.append('')

        return '\n'.join(header + body)

    # ── Tree walker ───────────────────────────────────────────

    def _walk(self, node: dict | None, lines: list, indent: int):
        if node is None:
            return

        mold  = node.get('mold',  '')
        block = node.get('block', '')
        p     = node.get('params', {})
        nid   = node.get('id', '')
        pad   = '    ' * indent

        # highlight call so the frontend can track execution
        lines.append(f'{pad}# {nid}')

        handler = getattr(self, f'_block_{mold}_{block}', None)
        if handler:
            handler(p, lines, indent)
        elif self._registry:
            self._community_block(mold, block, p, lines, indent)
        else:
            lines.append(f'{pad}pass  # unknown block {mold}.{block}')

        # recurse into the appropriate child(ren)
        if 'branches' in node:
            branches = node['branches']
            cond = self._build_condition(p)
            lines.append(f'{pad}if {cond}:')
            if branches.get('true'):
                self._walk(branches['true'], lines, indent + 1)
            else:
                lines.append(f'{pad}    pass')
            if branches.get('false'):
                lines.append(f'{pad}else:')
                self._walk(branches['false'], lines, indent + 1)
        elif 'body' in node:
            self._walk(node.get('body'), lines, indent + 1)
            self._walk(node.get('next'), lines, indent)
        else:
            self._walk(node.get('next'), lines, indent)

    # ── Condition builder (for branch blocks) ─────────────────

    def _build_condition(self, p: dict) -> str:
        left  = _val(p.get('left',  ''))
        right = _val(p.get('right', ''))
        op    = p.get('operator', '==')
        op_map = {'contains': 'in', 'not contains': 'not in'}
        op = op_map.get(op, op)
        if op in ('in', 'not in'):
            return f'{right} {op} {left}'
        return f'{left} {op} {right}'

    # ── variables mold ────────────────────────────────────────

    def _block_variables_declare(self, p, lines, indent):
        pad      = '    ' * indent
        name     = p.get('name', '_var')
        dtype    = p.get('dataType', 'text')
        raw_val  = p.get('value', '')

        type_cast = {'int': 'int', 'float': 'float', 'bool': 'bool'}.get(dtype, '')
        val = _val(raw_val) if raw_val.startswith('@') else _str_val(raw_val)

        if type_cast and not raw_val.startswith('@'):
            lines.append(f'{pad}{name} = {type_cast}({val})')
        else:
            lines.append(f'{pad}{name} = {val}')

    def _block_variables_assign(self, p, lines, indent):
        pad  = '    ' * indent
        target = p.get('target', '_var')
        val    = _val(p.get('value', '""'))
        lines.append(f'{pad}{target} = {val}')

    def _block_variables_modify(self, p, lines, indent):
        pad    = '    ' * indent
        target = p.get('target', '_var')
        op     = p.get('operator', '+=')
        val    = _val(p.get('value', '0'))
        lines.append(f'{pad}{target} {op} {val}')

    # ── io mold ───────────────────────────────────────────────

    def _block_io_print(self, p, lines, indent):
        pad = '    ' * indent
        val = _str_val(p.get('value', ''))
        lines.append(f'{pad}print({val})')

    def _block_io_prompt(self, p, lines, indent):
        pad    = '    ' * indent
        msg    = _str_val(p.get('message', ''))
        dtype  = p.get('dataType', 'text')
        target = p.get('target', '_inp')
        cast   = {'int': 'int', 'float': 'float'}.get(dtype, '')
        if cast:
            lines.append(f'{pad}{target} = {cast}(input({msg}))')
        else:
            lines.append(f'{pad}{target} = input({msg})')

    # ── control mold ──────────────────────────────────────────

    def _block_control_branch(self, p, lines, indent):
        pass   # condition emitted by _walk via _build_condition

    def _block_control_forLoop(self, p, lines, indent):
        pad  = '    ' * indent
        var  = p.get('variable', 'i')
        frm  = _val(p.get('from', '0'))
        to   = _val(p.get('to', '10'))
        step = _val(p.get('step', '1'))
        lines.append(f'{pad}for {var} in range({frm}, {to}, {step}):')

    def _block_control_forEachLoop(self, p, lines, indent):
        pad  = '    ' * indent
        var  = p.get('variable', 'item')
        lst  = _val(p.get('list', '[]'))
        lines.append(f'{pad}for {var} in {lst}:')

    def _block_control_whileLoop(self, p, lines, indent):
        pad  = '    ' * indent
        cond = self._build_condition(p)
        lines.append(f'{pad}while {cond}:')

    # ── math mold ─────────────────────────────────────────────

    def _block_math_arithmetic(self, p, lines, indent):
        pad    = '    ' * indent
        left   = _val(p.get('left',   '0'))
        right  = _val(p.get('right',  '0'))
        op     = p.get('operator', '+')
        result = p.get('result', '_res')
        lines.append(f'{pad}{result} = {left} {op} {right}')

    def _block_math_round(self, p, lines, indent):
        pad      = '    ' * indent
        val      = _val(p.get('value', '0'))
        decimals = _val(p.get('decimals', '0'))
        result   = p.get('result', '_res')
        lines.append(f'{pad}{result} = round({val}, {decimals})')

    def _block_math_abs(self, p, lines, indent):
        pad    = '    ' * indent
        val    = _val(p.get('value', '0'))
        result = p.get('result', '_res')
        lines.append(f'{pad}{result} = abs({val})')

    def _block_math_sqrt(self, p, lines, indent):
        pad    = '    ' * indent
        val    = _val(p.get('value', '0'))
        result = p.get('result', '_res')
        lines.append(f'{pad}{result} = _math.sqrt({val})')

    def _block_math_random(self, p, lines, indent):
        pad    = '    ' * indent
        mn     = _val(p.get('min', '0'))
        mx     = _val(p.get('max', '100'))
        result = p.get('result', '_res')
        lines.append(f'{pad}{result} = _random.randint({mn}, {mx})')

    # ── text mold ─────────────────────────────────────────────

    def _block_text_join(self, p, lines, indent):
        pad  = '    ' * indent
        left = _str_val(p.get('left', ''))
        right= _str_val(p.get('right', ''))
        sep  = _str_val(p.get('separator', ''))
        res  = p.get('result', '_res')
        lines.append(f'{pad}{res} = {sep}.join([str({left}), str({right})])')

    def _block_text_split(self, p, lines, indent):
        pad = '    ' * indent
        val = _str_val(p.get('value', ''))
        sep = _str_val(p.get('separator', ' '))
        res = p.get('result', '_res')
        lines.append(f'{pad}{res} = str({val}).split({sep})')

    def _block_text_upper(self, p, lines, indent):
        pad = '    ' * indent
        val = _str_val(p.get('value', ''))
        res = p.get('result', '_res')
        lines.append(f'{pad}{res} = str({val}).upper()')

    def _block_text_lower(self, p, lines, indent):
        pad = '    ' * indent
        val = _str_val(p.get('value', ''))
        res = p.get('result', '_res')
        lines.append(f'{pad}{res} = str({val}).lower()')

    def _block_text_replace(self, p, lines, indent):
        pad  = '    ' * indent
        val  = _str_val(p.get('value', ''))
        find = _str_val(p.get('find', ''))
        repl = _str_val(p.get('replaceWith', ''))
        res  = p.get('result', '_res')
        lines.append(f'{pad}{res} = str({val}).replace({find}, {repl})')

    def _block_text_length(self, p, lines, indent):
        pad = '    ' * indent
        val = _str_val(p.get('value', ''))
        res = p.get('result', '_res')
        lines.append(f'{pad}{res} = len(str({val}))')

    def _block_text_contains(self, p, lines, indent):
        pad    = '    ' * indent
        val    = _str_val(p.get('value', ''))
        search = _str_val(p.get('search', ''))
        res    = p.get('result', '_res')
        lines.append(f'{pad}{res} = {search} in str({val})')

    # ── collections mold ──────────────────────────────────────

    def _block_collections_createList(self, p, lines, indent):
        pad   = '    ' * indent
        items = p.get('items', '').strip()
        res   = p.get('result', '_list')
        if items:
            parts = [_str_val(i.strip()) for i in items.split(',')]
            lines.append(f'{pad}{res} = [{", ".join(parts)}]')
        else:
            lines.append(f'{pad}{res} = []')

    def _block_collections_append(self, p, lines, indent):
        pad  = '    ' * indent
        lst  = _val(p.get('list', '_list'))
        item = _str_val(p.get('item', ''))
        lines.append(f'{pad}{lst}.append({item})')

    def _block_collections_getItem(self, p, lines, indent):
        pad   = '    ' * indent
        lst   = _val(p.get('list', '_list'))
        idx   = _val(p.get('index', '0'))
        res   = p.get('result', '_item')
        lines.append(f'{pad}{res} = {lst}[{idx}]')

    def _block_collections_removeItem(self, p, lines, indent):
        pad = '    ' * indent
        lst = _val(p.get('list', '_list'))
        idx = _val(p.get('index', '0'))
        lines.append(f'{pad}del {lst}[{idx}]')

    def _block_collections_listLength(self, p, lines, indent):
        pad = '    ' * indent
        lst = _val(p.get('list', '_list'))
        res = p.get('result', '_len')
        lines.append(f'{pad}{res} = len({lst})')

    def _block_collections_createDict(self, p, lines, indent):
        pad = '    ' * indent
        res = p.get('result', '_dict')
        lines.append(f'{pad}{res} = {{}}')

    def _block_collections_setKey(self, p, lines, indent):
        pad  = '    ' * indent
        dct  = _val(p.get('dict', '_dict'))
        key  = _str_val(p.get('key', ''))
        val  = _str_val(p.get('value', ''))
        lines.append(f'{pad}{dct}[{key}] = {val}')

    def _block_collections_getKey(self, p, lines, indent):
        pad = '    ' * indent
        dct = _val(p.get('dict', '_dict'))
        key = _str_val(p.get('key', ''))
        res = p.get('result', '_val')
        lines.append(f'{pad}{res} = {dct}[{key}]')

    # ── functions mold ────────────────────────────────────────

    def _block_functions_define(self, p, lines, indent):
        pad    = '    ' * indent
        name   = p.get('name', '_fn')
        params = p.get('params', '').strip()
        lines.append(f'{pad}def {name}({params}):')

    def _block_functions_call(self, p, lines, indent):
        pad    = '    ' * indent
        name   = p.get('name', '_fn')
        args   = p.get('args', '').strip()
        result = p.get('result', '').strip()
        # resolve @var refs in args
        resolved = ', '.join(_val(a.strip()) for a in args.split(',')) if args else ''
        if result:
            lines.append(f'{pad}{result} = {name}({resolved})')
        else:
            lines.append(f'{pad}{name}({resolved})')

    def _block_functions_return(self, p, lines, indent):
        pad = '    ' * indent
        val = _val(p.get('value', ''))
        lines.append(f'{pad}return {val}')

    # ── Community mold dispatch ───────────────────────────────

    def _community_block(self, mold_name, block_id, p, lines, indent):
        """
        For community molds: look up pythonCall from the registry and generate
        a function call, routing outputs into named variables.
        """
        pad   = '    ' * indent
        block = self._registry.get_block(mold_name, block_id) if self._registry else None
        if not block or not block.get('pythonCall'):
            lines.append(f'{pad}pass  # no handler for {mold_name}.{block_id}')
            return

        fn_path = block['pythonCall']

        # Auto-import the top-level module (e.g. "mathex" from "mathex.average")
        module = fn_path.split('.')[0]
        if hasattr(self, '_community_imports'):
            self._community_imports.add(module)

        output_ids = {o['id'] for o in block.get('outputs', [])}
        args = ', '.join(
            f'{k}={_str_val(v)}' for k, v in p.items()
            if k not in output_ids
        )
        outputs = block.get('outputs', [])
        if outputs:
            result_var = p.get(outputs[0]['id'], '_result') or '_result'
            lines.append(f'{pad}{result_var} = {fn_path}({args})')
        else:
            lines.append(f'{pad}{fn_path}({args})')
