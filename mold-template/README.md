# Moldo Mold Template

A ready-to-use starter kit for building **Moldo molds** - installable block packages for the Moldo visual programming environment.

## What is a mold?

A mold adds new block types to the Moldo editor. Learners can drag your blocks onto the canvas just like built-in blocks. You write the Python logic; the Moldo manifest describes the UI.

## Quick start

### 1. Clone or download this template

```bash
# Download the template zip from the Moldo releases page, or clone and copy:
cp -r mold-template/ my-mold-name/
cd my-mold-name/
```

### 2. Rename the Python package

```bash
mv mymold/ my-mold-name/
```

Update every reference to `mymold` in `moldo.json` (`pythonCall` fields) to use your new package name.

### 3. Edit `moldo.json`

Fill in:

- `name` - machine identifier, lowercase, no spaces (e.g. `"webscraper"`)
- `displayName` - shown in the editor sidebar
- `description` - one-liner about what your mold does
- `author` - your name
- `blocks` - one entry per block you want to add

### 4. Implement your Python functions

Edit `my-mold-name/__init__.py`. Each `pythonCall` in `moldo.json` must map to a callable in your package:

```json
"pythonCall": "mypackage.do_something"
```

```python
# mypackage/__init__.py
def do_something(param1: str, result: str) -> ...:
    ...
```

> The `result` parameter is special - it's the variable name the user chose to store your output in. You don't need to return it; Moldo handles the assignment. Just return your computed value.

### 5. Add dependencies

List any pip packages your functions need in `requirements.txt`. They are installed automatically when a user installs your mold.

### 6. Pack it

```bash
zip -r my-mold-name.zip.mold moldo.json requirements.txt my-mold-name/
```

The file must have the `.zip.mold` extension.

### 7. Distribute

- Attach `my-mold-name.zip.mold` to a **GitHub Release** so users can download it directly
- Users install it in one click via **+ Install mold** in the editor toolbar

---

## moldo.json field reference

| Field                  | Required | Description                                      |
| ---------------------- | -------- | ------------------------------------------------ |
| `name`                 | yes      | Machine id - lowercase, no spaces                |
| `displayName`          | yes      | Sidebar label                                    |
| `version`              | yes      | SemVer string                                    |
| `description`          | yes      | One-line description                             |
| `author`               | yes      | Your name                                        |
| `moldoMinVersion`      | yes      | Minimum Moldo version required                   |
| `isCore`               | yes      | Always `false` for community molds               |
| `blocks[].id`          | yes      | Block identifier within this mold                |
| `blocks[].name`        | yes      | Block label in the sidebar                       |
| `blocks[].description` | yes      | Tooltip shown on hover                           |
| `blocks[].nodeType`    | yes      | `process`, `decision`, `output`, `loop`, `input` |
| `blocks[].nodeShape`   | yes      | `rect`, `diamond`, `circle`                      |
| `blocks[].color`       | yes      | Hex colour for the node accent bar               |
| `blocks[].inputs`      | yes      | Auto-generated settings form fields              |
| `blocks[].outputs`     | no       | Output variable fields                           |
| `blocks[].pythonCall`  | yes      | Dotted path to your Python callable              |
| `hasBranches`          | no       | `true` for if/else nodes                         |
| `hasBody`              | no       | `true` for loop/scope nodes                      |

### Input field types

| type       | Renders as   | Notes                                         |
| ---------- | ------------ | --------------------------------------------- |
| `text`     | Text input   | Free-form string                              |
| `variable` | Text input   | User types `@varName` to reference a variable |
| `number`   | Number input | Numeric value                                 |
| `select`   | Dropdown     | Provide `options: [...]` array                |
| `checkbox` | Checkbox     | Value is `"true"` or `"false"`                |

---

## Example: a full block definition

```json
{
  "id": "fetch",
  "name": "Fetch URL",
  "description": "Download text content from a URL",
  "nodeType": "process",
  "nodeShape": "rect",
  "color": "#f97316",
  "inputs": [
    {
      "id": "url",
      "label": "URL",
      "type": "variable",
      "placeholder": "@myUrl"
    },
    { "id": "timeout", "label": "Timeout (s)", "type": "number" }
  ],
  "outputs": [
    { "id": "result", "label": "Save result to", "type": "variable" }
  ],
  "pythonCall": "webscraper.fetch"
}
```

```python
# webscraper/__init__.py
import urllib.request

def fetch(url: str, timeout: str = "10") -> str:
    with urllib.request.urlopen(url, timeout=int(timeout)) as r:
        return r.read().decode()
```

---

## Tips

- Keep each function focused on one thing
- Use `str` for all params - Moldo passes everything as strings; cast inside your function
- Return `None` for blocks that only produce output (like `print`-style blocks)
- Return the computed value for blocks that have an `outputs` field - Moldo assigns it to the user's chosen variable name
- Test your functions with plain Python before packing the mold
