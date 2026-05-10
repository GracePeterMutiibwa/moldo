# Molds

A **mold** is a self-contained package that adds one or more new block types to the Moldo editor. Installing a mold makes its blocks immediately available in the sidebar - no restart needed.

---

## The 7 built-in molds

| Mold            | Colour  | Blocks                                                                                 |
| --------------- | ------- | -------------------------------------------------------------------------------------- |
| **variables**   | Blue    | Declare, Assign, Modify                                                                |
| **io**          | Amber   | Print, Prompt                                                                          |
| **control**     | Violet  | Branch, For Loop, For Each, While Loop                                                 |
| **math**        | Emerald | Arithmetic, Round, Abs, Sqrt, Random                                                   |
| **text**        | Pink    | Join, Split, Upper, Lower, Replace, Length, Contains                                   |
| **collections** | Orange  | Create List, Append, Get Item, Remove Item, List Length, Create Dict, Set Key, Get Key |
| **functions**   | Indigo  | Define, Call, Return                                                                   |

These are all implemented as molds - there is no special-casing in the runtime. Community molds work exactly the same way.

---

## Installing a community mold

1. Obtain a `.zip.mold` file from the mold's GitHub releases page
2. In the editor toolbar, click **+ Install mold**
3. Pick the `.zip.mold` file from disk
4. The backend extracts it, installs its Python dependencies, and the new blocks appear in the sidebar immediately

### From the API

```bash
curl -X POST http://127.0.0.1:8000/molds/install \
     -F "file=@webscraper.zip.mold"
```

---

## Uninstalling a mold

```bash
curl -X DELETE http://127.0.0.1:8000/molds/webscraper
```

Or restart the backend after manually deleting `moldo/installed/<mold-name>/`.

Built-in (core) molds cannot be uninstalled.

---

## Listing installed molds

```bash
curl http://127.0.0.1:8000/molds
```

Returns an array of manifests - one entry per installed mold, built-in and community alike.

---

## Creating your own mold

→ [Mold developer guide](creating-molds.md)
