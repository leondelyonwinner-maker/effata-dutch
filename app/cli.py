"""Operator CLI: `python -m app.cli hash-passcode "your-passcode"`.

Prints a bcrypt hash to stdout -- paste that (not the plaintext) into the
APP_PASSCODE_HASH environment variable on Render.
"""
import sys

from app.auth import hash_passcode


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] != "hash-passcode":
        print('Usage: python -m app.cli hash-passcode "your-passcode"', file=sys.stderr)
        raise SystemExit(1)
    print(hash_passcode(sys.argv[2]))


if __name__ == "__main__":
    main()
