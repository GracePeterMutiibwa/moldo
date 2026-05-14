# Runtime API

`moldo.runtime` exposes `compile_flow`, a pure Python function that converts an exported Moldo flow JSON into runnable Python source code. You can call it directly from any Python script without starting the backend server.

---

## `compile_flow(flow_json)`

```python
from moldo.runtime import compile_flow

python_source = compile_flow(flow_json)
```

**Parameters**

| Name | Type | Description |
| ---- | ---- | ----------- |
| `flow_json` | `dict` | The parsed contents of a `.json` file exported from mflow-editor |

**Returns**

A `str` containing valid Python source code equivalent to the visual flow.

**Side effects**

Prints the incoming JSON and the generated Python to stdout so you can inspect both without writing any files. This is intentional - useful during presentations and debugging.

---

## Example: compile and run from a script

```python
import json
from moldo.runtime import compile_flow

with open("average.json") as f:
    flow_json = json.load(f)

python_source = compile_flow(flow_json)

# Execute the generated code in an isolated namespace
exec(compile(python_source, "<flow>", "exec"), {})
```

---

## Example: compile and save

```python
import json
from pathlib import Path
from moldo.runtime import compile_flow

flow_json = json.loads(Path("myprogram.json").read_text())
python_source = compile_flow(flow_json)
Path("myprogram.py").write_text(python_source + "\n")
```

---

## Algorithm

`compile_flow` uses an iterative depth-first search over the flow node graph. It maintains an explicit stack so the recursion depth never depends on how deeply the flow is nested.

Each stack item is a typed tuple:

| Item shape | Meaning |
| ---------- | ------- |
| `('node', node_dict)` | Visit this flow node and push its children |
| `('emit', code_line)` | Write this line at the current indentation level |
| `('indent',)` | Increase indentation by one level (4 spaces) |
| `('dedent',)` | Decrease indentation by one level |

Nodes push their children in reverse order (since the stack is LIFO) so the first child is processed first.

---

## Community block resolution

When a community-block node has its manifest embedded in `flowObject.meta`, `compile_flow` reads the `pythonCall`, input slots, and output slots directly from it.

When the manifest is absent from `flowObject.meta` (some exports omit it there), the function checks `visualState.nodes[].settings` for the same node ID as a fallback.

If neither location has a manifest, the function applies a convention: any param whose value does **not** start with `@` is treated as an output variable name; everything that starts with `@` is an input variable reference. This correctly handles exports where only `moldName`, `blockId`, and `params` are present.

---

## Supported node types

| Node type | Notes |
| --------- | ----- |
| `declaration` | One assignment per variable in `meta` |
| `output` | `print()` call; f-string when `{var}` appears in message |
| `input` | `int/float/str/bool(input(...))` depending on `variableType` |
| `loop` | `for _loop_i in range(N):` with body indented |
| `decision` | `if` / `elif` chain; one branch per conditional in `meta.decisions` |
| `community-block` | `import module` prepended; result assigned to output variable(s) |
| `termination` | Silently ignored - marks visual end of flow |
