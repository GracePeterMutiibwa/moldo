import argparse
import sys
from pathlib import Path
from . import MoldoParser
from .api.server import app
import uvicorn


def compile_file(args):
    """Compile a Moldo file to Python."""
    parser = MoldoParser()
    with open(args.input, "r") as f:
        code = f.read()

    try:
        python_code, _ = parser.parse(code)
        if args.output:
            with open(args.output, "w") as f:
                f.write(python_code)
        else:
            print(python_code)
    except Exception as e:
        print(f"Error compiling file: {e}", file=sys.stderr)
        sys.exit(1)


def run_server(args):
    """Start the Moldo API server."""
    uvicorn.run(
        "moldo.api.server:app", host=args.host, port=args.port, reload=args.reload
    )


def main():
    parser = argparse.ArgumentParser(description="Moldo - Visual Programming Language")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Compile command
    compile_parser = subparsers.add_parser(
        "compile", help="Compile Moldo code to Python"
    )

    compile_parser.add_argument("input", help="Input Moldo file")

    compile_parser.add_argument("-o", "--output", help="Output Python file")

    compile_parser.set_defaults(func=compile_file)

    # Server command
    server_parser = subparsers.add_parser("serve", help="Start the Moldo API server")

    server_parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")

    server_parser.add_argument("--port", type=int, default=8000, help="Port to bind to")

    server_parser.add_argument(
        "--reload", action="store_true", help="Enable auto-reload"
    )
    server_parser.set_defaults(func=run_server)

    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
