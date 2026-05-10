# JSON Program Protocol

This document describes the JSON structure that the frontend editor sends to `POST /run`. Understanding it is useful if you want to build alternative editors, write tests, or debug compilation issues.

---

## Top-level structure

```json
{
  "version": "1.0",
  "molds": ["variables", "io", "control"],
  "program": { ... }
}
```

| Field     | Description                                            |
| --------- | ------------------------------------------------------ |
| `version` | Always `"1.0"` - reserved for future breaking changes  |
| `molds`   | Names of all molds whose blocks appear in this program |
| `program` | Root node - the first block that runs                  |

---

## Node structure

Every node follows this shape:

```json
{
  "id": "node-1",
  "mold": "io",
  "block": "print",
  "params": {
    "value": "@score"
  },
  "next": { ... }
}
```

| Field    | Description                                                     |
| -------- | --------------------------------------------------------------- |
| `id`     | Unique string identifier for this node (assigned by the canvas) |
| `mold`   | Mold name - e.g. `"io"`, `"variables"`, `"webscraper"`          |
| `block`  | Block id within the mold - e.g. `"print"`, `"declare"`          |
| `params` | Key-value map of the user's settings for this node              |
| `next`   | The next node to execute, or `null` if this is the last node    |

---

## Parameter values

Params are always strings. Two conventions:

| Syntax     | Meaning                                                                  |
| ---------- | ------------------------------------------------------------------------ |
| `"@score"` | Variable reference - resolves to the current value of `score`            |
| `"hello"`  | String literal - used as-is (wrapped in `repr()` for string contexts)    |
| `"42"`     | Numeric literal - used as-is; cast to int/float inside the block handler |

The `@` prefix tells the compiler to emit the bare identifier instead of a quoted string.

---

## Linear flow

Most blocks use `next` to chain:

```json
{
  "id": "node-1",
  "mold": "variables",
  "block": "declare",
  "params": { "name": "score", "value": "0", "dataType": "int" },
  "next": {
    "id": "node-2",
    "mold": "io",
    "block": "print",
    "params": { "value": "@score" },
    "next": null
  }
}
```

---

## Branching flow

Decision nodes use `branches` instead of `next`:

```json
{
  "id": "node-3",
  "mold": "control",
  "block": "branch",
  "params": {
    "left": "@score",
    "op": ">",
    "right": "5"
  },
  "branches": {
    "true": {
      "id": "node-4",
      "mold": "io",
      "block": "print",
      "params": { "value": "You win!" },
      "next": null
    },
    "false": {
      "id": "node-5",
      "mold": "io",
      "block": "print",
      "params": { "value": "Try again." },
      "next": null
    }
  },
  "next": {
    "id": "node-6",
    "mold": "io",
    "block": "print",
    "params": { "value": "Game over." },
    "next": null
  }
}
```

Both branches converge on `next` (if provided) after they finish executing.

**Supported operators:** `>`, `<`, `>=`, `<=`, `==`, `!=`

---

## Loop flow

Loop nodes use `body` for the repeated block chain and `next` for after the loop:

```json
{
  "id": "node-7",
  "mold": "control",
  "block": "forLoop",
  "params": {
    "variable": "i",
    "start": "0",
    "end": "10",
    "step": "1"
  },
  "body": {
    "id": "node-8",
    "mold": "io",
    "block": "print",
    "params": { "value": "@i" },
    "next": null
  },
  "next": {
    "id": "node-9",
    "mold": "io",
    "block": "print",
    "params": { "value": "Done!" },
    "next": null
  }
}
```

---

## Function definition

Function definition nodes are similar to loops - `body` holds the function body:

```json
{
  "id": "node-10",
  "mold": "functions",
  "block": "define",
  "params": {
    "name": "greet",
    "args": "name"
  },
  "body": {
    "id": "node-11",
    "mold": "io",
    "block": "print",
    "params": { "value": "@name" },
    "next": null
  },
  "next": {
    "id": "node-12",
    "mold": "functions",
    "block": "call",
    "params": { "name": "greet", "args": "Alice", "result": "_" },
    "next": null
  }
}
```

---

## Full program example

Declare a variable, loop 3 times, print the counter each iteration:

```json
{
  "version": "1.0",
  "molds": ["variables", "control", "io"],
  "program": {
    "id": "node-1",
    "mold": "variables",
    "block": "declare",
    "params": { "name": "count", "value": "0", "dataType": "int" },
    "next": {
      "id": "node-2",
      "mold": "control",
      "block": "forLoop",
      "params": { "variable": "i", "start": "1", "end": "4", "step": "1" },
      "body": {
        "id": "node-3",
        "mold": "io",
        "block": "print",
        "params": { "value": "@i" },
        "next": null
      },
      "next": null
    }
  }
}
```

Sends to `POST /run` and returns:

```json
{
  "ok": true,
  "output": "1\n2\n3\n",
  "highlights": ["node-1", "node-2", "node-3", "node-3", "node-3"]
}
```

---

## What the compiler does with this

`ProgramCompiler.compile(program)` walks the tree recursively and emits Python:

```python
import math as _math
import random as _random

# node-1
count = int(0)
# node-2
for i in range(1, 4, 1):
    # node-3
    print(i)
```

Each `# node-N` comment tells the execution tracker which node is currently running, so the editor can highlight it.
