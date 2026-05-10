# Moldo

**Moldo** is a visual educational programming language. Instead of writing text code, learners drag and connect **blocks** on a canvas to build programs. When they press **Run**, Moldo compiles the visual graph into Python and executes it - showing the output in real time.

<div class="grid cards" markdown>

- :material-puzzle-outline: **Block-based**

  Programs are built by connecting visual blocks. No syntax errors, no blank-page anxiety.

- :material-package-variant-closed: **Extensible via molds**

  Anyone can publish new block types as a `.zip.mold` package - no changes to the core needed.

- :material-school-outline: **Built for learning**

  Real Python under the hood. Learners build intuition about flow, variables, loops, and functions visually first.

- :material-api: **REST API**

  A FastAPI backend exposes everything over HTTP. Build your own editor or integration on top.

</div>

---

## How it works

```
  [mflow-editor]          [moldo backend]
  ─────────────           ───────────────
  Learner drags     →     Receives JSON
  and connects            program tree
  blocks on canvas
                    →     Compiles to
                          Python source
                    →     Executes and
                          streams output
  Shows output      ←
  and highlights
  active nodes
```

The **mflow-editor** is an Electron desktop app (plain HTML/JS, no framework). It talks to the **moldo** FastAPI backend over HTTP on `localhost:8000`.

---

## Quick start

=== "Backend"

    ```bash
    pip install moldo
    moldo serve
    # → running on http://127.0.0.1:8000
    ```

=== "From source"

    ```bash
    git clone https://github.com/GracePeterMutiibwa/moldo
    cd moldo
    python3 -m venv .venv && source .venv/bin/activate
    pip install -e .
    moldo serve
    ```

Then open the **mflow-editor** desktop app, drag some blocks, and press **Run**.

---

## What are molds?

A **mold** is a self-contained package that adds new block types to the editor. The 7 built-in capabilities (variables, I/O, control flow, math, text, collections, functions) are all molds - there is no special-casing.

Community developers can build and distribute molds for anything: web scraping, image processing, data analysis, hardware control, or game logic.

→ [Learn how to create a mold](molds/creating-molds.md)
