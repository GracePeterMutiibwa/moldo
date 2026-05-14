import argparse
import json
import sys
from pathlib import Path

import uvicorn

from moldo.runtime import compile_flow


def main():
    parser = argparse.ArgumentParser(
        prog='moldo',
        description='Moldo - Visual Programming Language CLI',
    )

    parser.add_argument('input_json', nargs='?', metavar='INPUT_JSON',
                        help='Exported flow JSON file')
    parser.add_argument('-c', '--compile', metavar='INPUT_JSON',
                        help='Exported flow JSON file (flag form, same as positional)')
    parser.add_argument('-o', '--output', metavar='OUTPUT_PY',
                        help='Write generated Python here (default: print to stdout)')
    parser.add_argument('--serve', action='store_true',
                        help='Start the Moldo API server instead of compiling')
    parser.add_argument('--host', default='127.0.0.1', help='Server host (with --serve)')
    parser.add_argument('--port', type=int, default=8000, help='Server port (with --serve)')
    parser.add_argument('--reload', action='store_true', help='Auto-reload (with --serve)')

    args = parser.parse_args()

    if args.serve:
        uvicorn.run('moldo.api.server:app',
                    host=args.host, port=args.port, reload=args.reload)
        return

    input_file = args.compile or args.input_json
    if not input_file:
        parser.print_help()
        sys.exit(1)

    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    try:
        flow_json = json.loads(input_path.read_text())
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        python_source = compile_flow(flow_json)
    except Exception as exc:
        print(f"Error: compilation failed: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(python_source + '\n')
        print(f"Written to {output_path}")
    else:
        print(python_source)


if __name__ == '__main__':
    main()
