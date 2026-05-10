# Manifest Reference

Every mold is described by a `moldo.json` file. This document is a complete field-by-field reference.

---

## Top-level fields

```json
{
  "name": "webscraper",
  "displayName": "Web Scraper",
  "version": "1.0.0",
  "description": "Fetch and extract content from web pages",
  "author": "Your Name",
  "moldoMinVersion": "0.5.0",
  "isCore": false,
  "blocks": [ ... ]
}
```

| Field             | Type    | Required | Description                                                                                             |
| ----------------- | ------- | -------- | ------------------------------------------------------------------------------------------------------- |
| `name`            | string  | yes      | Machine identifier - lowercase, no spaces, no hyphens. Used as the import name for your Python package. |
| `displayName`     | string  | yes      | Human-readable name shown in the sidebar group header.                                                  |
| `version`         | string  | yes      | SemVer string - `"1.0.0"`.                                                                              |
| `description`     | string  | yes      | One-line description shown on hover.                                                                    |
| `author`          | string  | yes      | Your name or organisation.                                                                              |
| `moldoMinVersion` | string  | yes      | The minimum Moldo version your mold requires. Use `"0.5.0"` for now.                                    |
| `isCore`          | boolean | yes      | `false` for all community molds.                                                                        |
| `blocks`          | array   | yes      | One entry per block type.                                                                               |

---

## Block fields

```json
{
  "id": "fetch",
  "name": "Fetch Page",
  "description": "Download text from a URL",
  "nodeType": "process",
  "nodeShape": "rect",
  "color": "#f97316",
  "icon": "globe",
  "hasBranches": false,
  "hasBody": false,
  "inputs": [ ... ],
  "outputs": [ ... ],
  "pythonCall": "webscraper.fetch_page"
}
```

| Field         | Type    | Required             | Description                                                               |
| ------------- | ------- | -------------------- | ------------------------------------------------------------------------- |
| `id`          | string  | yes                  | Block identifier within this mold - unique per mold.                      |
| `name`        | string  | yes                  | Block label shown in the sidebar and on the node.                         |
| `description` | string  | yes                  | Tooltip shown when hovering in the sidebar.                               |
| `nodeType`    | string  | yes                  | Semantic type - see below.                                                |
| `nodeShape`   | string  | yes                  | Visual shape - see below.                                                 |
| `color`       | string  | yes                  | Hex colour for the node accent bar (`"#f97316"`).                         |
| `icon`        | string  | no                   | Icon identifier (Bootstrap Icons name or short alias).                    |
| `hasBranches` | boolean | no                   | `true` for decision/if nodes - canvas draws true/false ports.             |
| `hasBody`     | boolean | no                   | `true` for loop and function-definition nodes - canvas draws a body port. |
| `inputs`      | array   | yes                  | Form fields shown in the settings panel.                                  |
| `outputs`     | array   | no                   | Output variable slots.                                                    |
| `pythonCall`  | string  | community molds only | Dotted path to your Python callable: `"package.function"`.                |

### `nodeType` values

| Value      | Meaning                                             |
| ---------- | --------------------------------------------------- |
| `process`  | Transforms data - one input port, one output port   |
| `decision` | Branches on a condition - needs `hasBranches: true` |
| `output`   | Produces visible output (print, draw, etc.)         |
| `loop`     | Repeats a body - needs `hasBody: true`              |
| `input`    | Reads from the user                                 |

### `nodeShape` values

| Value     | Visual                                       |
| --------- | -------------------------------------------- |
| `rect`    | Rectangle with left accent bar (default)     |
| `diamond` | Rotated square - use for decision nodes      |
| `circle`  | Round pill - use for return / terminal nodes |

---

## Input field schema

```json
{
  "id": "url",
  "label": "URL",
  "type": "variable",
  "placeholder": "@myUrl",
  "options": []
}
```

| Field         | Type   | Required          | Description                                             |
| ------------- | ------ | ----------------- | ------------------------------------------------------- |
| `id`          | string | yes               | Parameter key - passed to your Python function by name. |
| `label`       | string | yes               | Label shown above the field in the settings panel.      |
| `type`        | string | yes               | Field type - see below.                                 |
| `placeholder` | string | no                | Placeholder text.                                       |
| `options`     | array  | only for `select` | List of string options for the dropdown.                |

### Input types

| type       | Renders as   | Value sent to Python                          |
| ---------- | ------------ | --------------------------------------------- |
| `text`     | Text input   | String as typed                               |
| `variable` | Text input   | `@varName` → bare identifier in compiled code |
| `number`   | Number input | String (cast inside your function)            |
| `select`   | Dropdown     | One of the `options` strings                  |
| `checkbox` | Checkbox     | `"true"` or `"false"`                         |

---

## Output field schema

```json
{
  "id": "result",
  "label": "Save result to",
  "type": "variable"
}
```

Outputs always have `type: "variable"`. The user types a variable name. The compiler generates `variable_name = pythonCall(...)` using the return value of your function.

---

## Complete example

```json
{
  "name": "imgtools",
  "displayName": "Image Tools",
  "version": "1.0.0",
  "description": "Basic image operations using Pillow",
  "author": "Grace Peter",
  "moldoMinVersion": "0.5.0",
  "isCore": false,
  "blocks": [
    {
      "id": "resize",
      "name": "Resize Image",
      "description": "Scale an image to a new width and height",
      "nodeType": "process",
      "nodeShape": "rect",
      "color": "#8b5cf6",
      "inputs": [
        { "id": "path", "label": "Image path", "type": "variable" },
        { "id": "width", "label": "Width (px)", "type": "number" },
        { "id": "height", "label": "Height (px)", "type": "number" }
      ],
      "outputs": [
        { "id": "result", "label": "Save path to", "type": "variable" }
      ],
      "pythonCall": "imgtools.resize"
    },
    {
      "id": "grayscale",
      "name": "Grayscale",
      "description": "Convert an image to grayscale",
      "nodeType": "process",
      "nodeShape": "rect",
      "color": "#8b5cf6",
      "inputs": [{ "id": "path", "label": "Image path", "type": "variable" }],
      "outputs": [
        { "id": "result", "label": "Save path to", "type": "variable" }
      ],
      "pythonCall": "imgtools.grayscale"
    }
  ]
}
```
