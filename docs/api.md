# API Reference

The Moldo backend exposes a REST API on `http://127.0.0.1:8000` by default.

All request and response bodies are JSON unless stated otherwise.

---

## `GET /health`

Health check. Used by the editor to show the connection status indicator.

**Response**

```json
{ "status": "ok" }
```

---

## `POST /run`

Compile and execute a JSON program tree.

**Request body**

```json
{
  "version": "1.0",
  "molds": ["variables", "io", "control"],
  "program": { ... }
}
```

| Field     | Type     | Description                                                 |
| --------- | -------- | ----------------------------------------------------------- |
| `version` | string   | Protocol version - always `"1.0"`                           |
| `molds`   | string[] | List of mold names used in this program                     |
| `program` | object   | Root node of the program tree - see [Protocol](protocol.md) |

**Success response**

```json
{
  "ok": true,
  "output": "Hello\n10\n",
  "highlights": ["node-1", "node-2", "node-3"]
}
```

**Error response**

```json
{
  "ok": false,
  "error": "NameError: name 'score' is not defined",
  "highlights": ["node-2"]
}
```

`highlights` contains the IDs of nodes that were reached before the error occurred. The editor uses these to animate execution.

---

## `GET /molds`

List all installed molds - built-ins and community molds alike.

**Response** - array of manifest objects

```json
[
  {
    "name": "variables",
    "displayName": "Variables",
    "version": "1.0.0",
    "isCore": true,
    "blocks": [ ... ]
  },
  {
    "name": "webscraper",
    "displayName": "Web Scraper",
    "version": "1.2.0",
    "isCore": false,
    "blocks": [ ... ]
  }
]
```

---

## `POST /molds/install`

Upload and install a `.zip.mold` package.

**Request** - `multipart/form-data`

| Field  | Type | Description          |
| ------ | ---- | -------------------- |
| `file` | file | The `.zip.mold` file |

```bash
curl -X POST http://127.0.0.1:8000/molds/install \
     -F "file=@webscraper.zip.mold"
```

**Success response**

```json
{
  "ok": true,
  "manifest": {
    "name": "webscraper",
    "displayName": "Web Scraper",
    "version": "1.2.0",
    "blocks": [ ... ]
  }
}
```

**Error response**

```json
{
  "ok": false,
  "error": "moldo.json not found in archive"
}
```

### What happens during install

1. The zip is extracted to `moldo/installed/<name>/`
2. `moldo.json` is validated (must be present and parseable)
3. `pip install -r requirements.txt` is run (if `requirements.txt` exists)
4. The manifest is registered in the in-memory mold registry
5. The manifest is returned so the frontend can register the blocks immediately

---

## `DELETE /molds/{name}`

Uninstall a community mold.

**Path parameter** - `name`: the mold's machine identifier (e.g. `webscraper`)

```bash
curl -X DELETE http://127.0.0.1:8000/molds/webscraper
```

**Success response**

```json
{ "ok": true }
```

**Error responses**

```json
{ "ok": false, "error": "Mold 'webscraper' not found" }
{ "ok": false, "error": "Cannot uninstall core mold 'variables'" }
```

Core molds (built-ins) cannot be uninstalled.

---

## Running on a different port

```bash
uvicorn moldo.api.server:app --host 127.0.0.1 --port 8001
```

Update `const BACKEND` in `mflow-editor/index.html` to match.

---

## CORS

The server allows all origins (`*`) so the editor (which loads as a `file://` URL in Electron) can reach it without CORS errors.

!!! warning "Do not expose to the network"
The `/run` endpoint executes arbitrary Python code. Keep the backend bound to `127.0.0.1`. Do not expose it on `0.0.0.0` or forward port 8000 through a firewall.
