# Moldo

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/moldo/badge/?version=latest)](https://moldo.readthedocs.io/en/latest/?badge=latest)

> Visual educational programming - block-based, Python-powered, extensible.

Moldo is the backend runtime for a visual block-based programming environment. Learners drag and connect blocks in the **mflow-editor** desktop app to build programs. The editor compiles the visual graph to a JSON program tree and sends it to this backend, which executes it and streams the output back.

The system is extensible through **molds** - self-contained `.zip.mold` packages that add new block types to the editor. The 7 built-in capabilities (variables, I/O, control, math, text, collections, functions) are themselves molds.

---

## Installation

```bash
pip install moldo
moldo serve
```

Or from source:

```bash
git clone https://github.com/GracePeterMutiibwa/moldo
cd moldo
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
moldo serve
```

The backend runs at `http://127.0.0.1:8000`. Open **mflow-editor** and the green dot in the toolbar confirms the connection.

---

## API

| Endpoint               | Description                      |
| ---------------------- | -------------------------------- |
| `GET /health`          | Health check                     |
| `POST /run`            | Execute a JSON program tree      |
| `GET /molds`           | List installed molds             |
| `POST /molds/install`  | Upload and install a `.zip.mold` |
| `DELETE /molds/{name}` | Uninstall a community mold       |

Full API docs → [docs/api.md](docs/api.md) or run `mkdocs serve` for the rendered site.

---

## Molds

A mold adds new block types to the editor. Install any `.zip.mold` from the editor toolbar - no restart required.

To build your own mold:

1. Download the [mold-template](mold-template/) from this repository
2. Follow the [mold developer guide](docs/molds/creating-molds.md)
3. Pack and attach to a GitHub Release

---

## Documentation

```bash
pip install mkdocs-material
mkdocs serve
```

Then open `http://127.0.0.1:8000` to browse the full documentation site.

## License

MIT - see [LICENSE](LICENSE)

## Author

Grace Peter Mutiibwa · [gracepeter.clearnique.com](https://gracepeter.clearnique.com) · [GitHub](https://github.com/GracePeterMutiibwa)
