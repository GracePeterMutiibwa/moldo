# Creating Molds - Developer Guide

This guide walks you from zero to a working, installable mold. By the end you will have a `.zip.mold` file that anyone can install with one click in the Moldo editor.

---

## The big picture

A mold is a **zip file with a `.zip.mold` extension** containing:

```
my-mold.zip.mold
├── moldo.json          ← manifest: describes your blocks and their UI
├── requirements.txt    ← pip dependencies (can be empty)
└── mypackage/          ← your Python package
    └── __init__.py     ← your block functions live here
```

The manifest and the Python code are the only two moving parts. The manifest drives the editor UI; the Python code drives execution.

---

## Step 0 - Get the template

Download the [mold-template](https://github.com/GracePeterMutiibwa/moldo/tree/main/mold-template) from the Moldo repository (the folder is also downloadable as a zip via the GitHub UI: **Code → Download ZIP** while browsing the `mold-template/` directory).

```bash
# Or copy from a local moldo checkout:
cp -r moldo/mold-template/ my-mold/
cd my-mold/
mv mymold/ mypackage/          # rename the Python package
```

---

## Step 1 - Design your blocks

Before writing any code, sketch on paper (or in your head):

- What are the block **inputs**? (what the user configures in the settings panel)
- Does the block **produce a value**? (shown as an output variable slot)
- What **node type** fits? `process` transforms data; `output` prints/draws; `input` reads from the user

Aim for **one block = one clear action**. Avoid Swiss-army-knife blocks.

### Node types and shapes quick-pick

| I want a block that…                   | nodeType     | nodeShape |
| -------------------------------------- | ------------ | --------- |
| transforms data and stores a result    | `process`    | `rect`    |
| prints / draws / plays something       | `output`     | `rect`    |
| asks the user a question               | `input`      | `rect`    |
| branches the flow based on a condition | `decision`   | `diamond` |
| loops over something                   | `loop`       | `rect`    |
| marks the end of a function            | _(terminal)_ | `circle`  |

---

## Step 2 - Write `moldo.json`

The manifest has two parts: **mold metadata** and a **blocks array**.

```json
{
  "name": "weather",
  "displayName": "Weather",
  "version": "1.0.0",
  "description": "Look up current weather for any city",
  "author": "Grace Peter",
  "moldoMinVersion": "0.5.0",
  "isCore": false,
  "blocks": [
    {
      "id": "current",
      "name": "Current Weather",
      "description": "Returns temperature and conditions for a city",
      "nodeType": "process",
      "nodeShape": "rect",
      "color": "#0ea5e9",
      "inputs": [
        {
          "id": "city",
          "label": "City",
          "type": "variable",
          "placeholder": "@cityName"
        },
        {
          "id": "unit",
          "label": "Unit",
          "type": "select",
          "options": ["celsius", "fahrenheit"]
        }
      ],
      "outputs": [
        {
          "id": "result",
          "label": "Save result to",
          "type": "variable"
        }
      ],
      "pythonCall": "weather.current"
    }
  ]
}
```

#### Key rules

- `name` must match your Python package folder name exactly - it is used as the import path
- `pythonCall` is `"<package>.<function>"` - must be importable from your package
- Every `inputs[].id` becomes a keyword argument in your Python function call
- Every `outputs[].id` maps to the variable name the user picks; Moldo generates `varname = yourfunction(...)`

---

## Step 3 - Implement the Python functions

```python
# weather/__init__.py
import urllib.request
import json

def current(city: str, unit: str = "celsius") -> str:
    """Return a summary string like '22°C, partly cloudy'."""
    # Demo: real implementation would call a weather API
    return f"Weather for {city}: 22{'°C' if unit == 'celsius' else '°F'}, sunny"
```

### Function signature rules

1. **Every `inputs[].id` is a keyword argument** - use the exact same name
2. **All parameters are strings** - Moldo passes everything as strings. Cast inside your function (`int(width)`, `float(timeout)`)
3. **Return `None`** for output-only blocks (print, draw). Moldo does not assign the return value
4. **Return a value** for process blocks that have `outputs[]`. Moldo assigns it to the user's chosen variable name

```python
# Output-only block - returns None
def greet(name: str, style: str = "casual") -> None:
    if style == "shout":
        print(f"HEY {name.upper()}!!!")
    else:
        print(f"Hello, {name}!")

# Process block with output - returns a value
def reverse_text(text: str) -> str:
    return text[::-1]
```

### Accessing variables

When a user types `@myVar` in an input field, Moldo resolves it to the current value of that variable before calling your function. You receive the already-resolved value - just treat it as a regular string (or cast it to the type you need).

---

## Step 4 - List your dependencies

```
# requirements.txt
requests>=2.31
```

Leave the file empty if you only use the Python standard library. Moldo runs `pip install -r requirements.txt` automatically during install.

---

## Step 5 - Test locally

Test your functions in isolation before packing:

```python
# test_weather.py
from weather import current

print(current("Kampala", "celsius"))
# → Weather for Kampala: 22°C, sunny

print(current("London", "fahrenheit"))
# → Weather for London: 22°F, sunny
```

```bash
python test_weather.py
```

No need to run Moldo for this step - plain Python is faster for iteration.

---

## Step 6 - Pack the mold

```bash
zip -r weather.zip.mold moldo.json requirements.txt weather/
```

!!! warning "Extension matters"
The file **must** end in `.zip.mold`. The editor's file picker filters for this extension.

Verify the zip contents:

```bash
unzip -l weather.zip.mold
# Archive:  weather.zip.mold
#   moldo.json
#   requirements.txt
#   weather/__init__.py
```

---

## Step 7 - Test the full install flow

1. Start the Moldo backend (`moldo serve`)
2. Open the editor
3. Click **+ Install mold** in the toolbar
4. Pick `weather.zip.mold`
5. The output panel should show `✓ Mold "Weather" installed`
6. **Weather** appears in the sidebar - drag a **Current Weather** block onto the canvas
7. Double-click the node to open the settings panel - confirm your inputs render correctly
8. Wire it up and press **Run**

---

## Step 8 - Distribute via GitHub

The recommended distribution channel is a **GitHub Release**:

1. Push your mold source to a public GitHub repository
2. Create a release (`Releases → Draft a new release`)
3. Attach `weather.zip.mold` as a release asset
4. Users download it directly from the release page

Your repository structure should look like:

```
weather-mold/               ← GitHub repo root
├── README.md               ← short description + install instructions
├── moldo.json              ← manifest (also at zip root)
├── requirements.txt
└── weather/
    └── __init__.py
```

Put a one-liner install instruction in `README.md`:

```markdown
## Install

1. Download `weather.zip.mold` from [Releases](https://github.com/you/weather-mold/releases)
2. In Moldo editor → **+ Install mold** → pick the file
```

---

## Common patterns

### A block with multiple outputs

```json
"outputs": [
  { "id": "temperature", "label": "Temperature",  "type": "variable" },
  { "id": "conditions",  "label": "Conditions",   "type": "variable" }
]
```

```python
def current(city: str) -> tuple:
    return (22.0, "sunny")
    # Moldo unpacks: temperature, conditions = current(city=...)
```

### A decision block

```json
{
  "id": "is_above",
  "name": "Value Above Threshold",
  "nodeType": "decision",
  "nodeShape": "diamond",
  "hasBranches": true,
  "inputs": [
    { "id": "value", "label": "Value", "type": "variable" },
    { "id": "threshold", "label": "Threshold", "type": "number" }
  ],
  "pythonCall": "mypackage.is_above"
}
```

```python
def is_above(value: str, threshold: str) -> bool:
    return float(value) > float(threshold)
    # Moldo uses the boolean to route true/false branches
```

### A loop block

```json
{
  "id": "repeat",
  "name": "Repeat N Times",
  "nodeType": "loop",
  "nodeShape": "rect",
  "hasBody": true,
  "inputs": [{ "id": "times", "label": "Times", "type": "number" }],
  "pythonCall": "mypackage.repeat_range"
}
```

```python
def repeat_range(times: str):
    return range(int(times))
    # Moldo generates: for _ in repeat_range(times=...): <body>
```

---

## Checklist before publishing

- [ ] `name` in `moldo.json` matches the Python package folder name
- [ ] Every `pythonCall` is importable: `python3 -c "from weather import current"`
- [ ] All function params match `inputs[].id` exactly
- [ ] Functions cast string params to the types they need
- [ ] `requirements.txt` lists all non-stdlib dependencies
- [ ] Zip root contains `moldo.json`, `requirements.txt`, and your package folder
- [ ] File extension is `.zip.mold`
- [ ] Full install + run tested locally
- [ ] GitHub release created with `.zip.mold` attached
