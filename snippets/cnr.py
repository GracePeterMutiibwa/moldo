#!/usr/bin/env python3
"""
Script to compile and run a Moldo file using our modified parser.
"""

import os
import sys
from ..moldo import MoldoParser


def main():
    """
    Compile and run a Moldo file.
    """
    if len(sys.argv) < 2:
        print("Usage: python cnr.py <moldo_file>")
        sys.exit(1)

    moldo_file = sys.argv[1]

    if not os.path.exists(moldo_file):
        print(f"File not found: {moldo_file}")
        sys.exit(1)

    # Read the Moldo file
    with open(moldo_file, "r", encoding="utf-8") as f:
        moldo_code = f.read()

    # Compile the Moldo code
    parser = MoldoParser()

    try:
        python_code, _ = parser.parse(moldo_code)
    except Exception as e:
        print(f"Error compiling Moldo code: {e}")
        sys.exit(1)

    # Generate the Python file path
    py_file = os.path.splitext(moldo_file)[0] + ".py"

    # Write the Python code to a file
    with open(py_file, "w", encoding="utf-8") as f:
        f.write(python_code)

    print(f"Compiled {moldo_file} to {py_file}")

    # Run the compiled Python code
    print("\n--- Running the compiled code ---\n")
    try:
        with open(py_file, "r", encoding="utf-8") as f:
            python_code = f.read()
        exec(python_code)
    except Exception as e:
        print(f"Error running compiled code: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
