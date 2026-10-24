"""Interactive version (numbered menus); the engine is shared with the flag-based CLI."""

import os
import sys


def main() -> None:
    if not sys.stdin.isatty():
        print("Error: the menu needs an interactive terminal; use `dorkint <mode> ...`.", file=sys.stderr)
        raise SystemExit(2)
    from dorkint.tui import flow  # late import: flow imports cli, which imports this package

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # braille outside the console encoding: no crash
    os.system("")  # enables ANSI escapes (screen clear) on the Windows console
    flow.show_banner(print)
    try:
        flow.run()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye.")
