"""Only menu module that touches `input()`; I/O is injectable for tests."""

import sys
from collections.abc import Callable, Sequence

from dorkint.visual import render_menu

InputFn = Callable[[str], str]
PrintFn = Callable[[str], None]


def choose(
    title: str,
    options: Sequence[str],
    *,
    hints: Sequence[str] = (),
    back: str = "Back",
    input_fn: InputFn = input,
    print_fn: PrintFn = print,
) -> int | None:
    """Numbered menu; returns the 0-based index of the option, or None for `q` (back)."""
    print_fn("\n" + render_menu(title, options, hints=hints, back=back, color=sys.stdout.isatty()))
    while True:
        entry = input_fn("> ").strip()
        if entry.lower() == "q":
            return None
        if entry.isdigit() and 1 <= int(entry) <= len(options):
            return int(entry) - 1
        print_fn(f"Invalid choice: enter a number between 1 and {len(options)}, or q.")


def ask(
    label: str,
    *,
    optional: bool = True,
    input_fn: InputFn = input,
    print_fn: PrintFn = print,
) -> str:
    """Free input; ENTER returns "" if `optional`, otherwise asks again."""
    prompt_text = f"{label} (ENTER to skip) : " if optional else f"{label} : "
    while True:
        entry = input_fn(prompt_text).strip()
        if entry or optional:
            return entry
        print_fn("A value is required.")
