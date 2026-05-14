# Getting Started

## Requirements

- Python 3.10 or later
- Node.js 18 or later (for the visual editor)

---

## 1. Install the backend

=== "From PyPI"

    ```bash
    pip install moldo
    ```

=== "From source"

    ```bash
    git clone https://github.com/GracePeterMutiibwa/moldo
    cd moldo
    python3 -m venv .venv
    source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install -e .
    ```

---

## 2. Start the backend server

```bash
moldo --serve
```

You should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Confirm it is healthy:

```bash
curl http://127.0.0.1:8000/health
# → {"status":"ok"}
```

---

## 3. Open the editor

Download and open **mflow-editor** from the [releases page](https://github.com/GracePeterMutiibwa/moldo/releases).

Or run it from source:

```bash
git clone https://github.com/GracePeterMutiibwa/mflow-editor
cd mflow-editor
npm install
npm start
```

The toolbar shows a green dot when the editor has successfully connected to your backend.

---

## 4. Build your first program

Let's print the numbers 1 to 5.

1. In the sidebar, expand **Variables** and drag a **Declare Variable** block onto the canvas. Set `name = i`, `type = int`, `value = 1`.
2. Expand **Control** and drag a **While Loop** block. Set `left = @i`, `op = <=`, `right = 5`.
3. Expand **I/O** and drag a **Print** block. Set `value = @i`. Connect it as the loop body.
4. Expand **Variables** and drag a **Modify Variable** block. Set `name = @i`, `op = +`, `operand = 1`. Connect it after Print inside the loop body.
5. Press **Run**.

The output panel shows:

```
1
2
3
4
5
```

---

## Compile a flow to Python

After building a program in the editor, export it from **File > Export** and compile it from the terminal:

```bash
moldo myprogram.json            # print generated Python to stdout
moldo -c myprogram.json -o myprogram.py   # write to a file
python myprogram.py             # run it standalone
```

See the [CLI Reference](cli.md) for all options.

---

## Development mode

Run the backend with auto-reload (restarts on file changes):

```bash
moldo --serve --reload
```

Run the editor with the Node.js inspector:

```bash
npm run dev
```

---

## Troubleshooting

**Editor shows red dot / "backend offline"**
: The backend is not running or not reachable at `http://127.0.0.1:8000`. Check that `moldo serve` is running and that no firewall is blocking localhost.

**`ModuleNotFoundError: No module named 'moldo'`**
: Run `pip install -e .` inside the moldo directory (with your virtualenv active).

**Port 8000 already in use**
: `uvicorn moldo.api.server:app --port 8001` and update `const BACKEND` in `index.html` to match.
