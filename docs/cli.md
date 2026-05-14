# CLI Reference

The `moldo` command is installed alongside the Python package and gives you two capabilities: compiling exported flow JSON to Python source code and starting the backend API server.

---

## Compile a flow to Python

Take a `.json` file exported from mflow-editor and turn it into a runnable Python script.

**Positional form - print to stdout**

```bash
moldo myprogram.json
```

**Flag form - same result**

```bash
moldo -c myprogram.json
```

**Write to a file with `-o`**

```bash
moldo -c myprogram.json -o myprogram.py
python myprogram.py
```

Both `-c` and the positional form accept the same file. Use whichever feels more natural.

---

## How export works

Inside mflow-editor, use **File > Export** (or the export button in the toolbar). This saves a `.json` file that captures the full flow graph. Pass that file directly to `moldo`.

The CLI reads the `flowObject` section of the exported JSON, walks the node graph using an iterative depth-first search, and emits equivalent Python code.

---

## What gets generated

| Flow node type | Generated Python |
| -------------- | ---------------- |
| Declaration | `variable = default_value` |
| Input | `variable = int(input("prompt"))` |
| Output | `print("message")` or `print(f"message {var}")` |
| Loop | `for _loop_i in range(N):` |
| Decision | `if condition:` / `elif condition:` |
| Community block | `import module` + `result = module.function(args)` |

### Example

Given this flow: declare `x = 0`, prompt the user for `x`, print `"You entered {x}"`.

```bash
moldo prompt-demo.json
```

Output:

```python
x = 0
x = int(input("Enter a number"))
print(f"You entered {x}")
```

---

## Debug output

`compile_flow` always prints the incoming JSON and the generated Python to stdout so you can verify both sides:

```
=== INPUT JSON ===
{ ... }

=== GENERATED PYTHON ===
x = 0
...
```

When you use `-o` to write to a file, the debug output still appears in the terminal and the clean Python is written to the file.

---

## Start the API server

```bash
moldo --serve
```

Optional flags:

| Flag | Default | Description |
| ---- | ------- | ----------- |
| `--host` | `127.0.0.1` | Address to bind to |
| `--port` | `8000` | Port to listen on |
| `--reload` | off | Auto-restart on source changes |

```bash
moldo --serve --port 8001 --reload
```

---

## Using the Python API directly

If you want to call `compile_flow` from your own script instead of the CLI, see the [Runtime API](runtime.md) page.
