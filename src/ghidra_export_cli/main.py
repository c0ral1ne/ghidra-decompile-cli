import os
import argparse
import pyghidra
from .utils import GhidraExport, load_program


PROJECT_DIR = "/tmp/ghidra-export-cli"
PROJECT_NAME = "ghidra_export"


def initialize():
    parser = argparse.ArgumentParser(
        prog="gdecompile",
        description="Decompile binary programs using pyghidra and output results to stdout (default)",
    )
    parser.add_argument("binary_path")
    parser.add_argument(
        "-o", "--output", help="store results in output file instead of print to stdout"
    )
    parser.add_argument(
        "-a",
        help="include all functions (thunk functions, stubs, etc.)",
        action="store_true",
    )
    args = parser.parse_args()

    # Create project directory in /tmp
    try:
        os.makedirs(PROJECT_DIR, exist_ok=True)
    except OSError as e:
        print(f"Error making project directory: {e}")
        exit(1)

    return args


def main():
    args = initialize()

    try:
        pyghidra.start()
    except ValueError as e:
        print(e)
        exit(1)

    with pyghidra.open_project(PROJECT_DIR, PROJECT_NAME, create=True) as project:
        program = load_program(project, os.path.abspath(args.binary_path))
        ghidra_export = GhidraExport(project, program)

        decompiled = ghidra_export.decompile_source_formatted(
            ghidra_export.decompile(args.a)
        )
        if args.output:
            with open(os.path.abspath(args.output), "w") as f:
                f.write(decompiled)
            print(f"Finished decompiling, wrote output to {args.output}")
        else:
            print(decompiled)


if __name__ == "__main__":
    main()
