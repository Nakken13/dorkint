"""Menu flow: mode -> value -> refinements -> keyword -> results. No direct I/O."""

from pathlib import Path

from dorkint.banner import banner
from dorkint.builder import DorkintError, generate, get_mode
from dorkint.cli import MODES
from dorkint.output import format_dorks, save
from dorkint.tui.prompts import InputFn, PrintFn, ask, choose

_REFINEMENT_LABELS = {"city": "Known city", "company": "Known company"}


def _search(mode: str, input_fn: InputFn, print_fn: PrintFn) -> str | None:
    """Asks the mode's questions; returns the results text, or None if an error was shown."""
    if mode == "fullname":
        first = ask("First name", optional=False, input_fn=input_fn, print_fn=print_fn)
        last = ask("Last name", optional=False, input_fn=input_fn, print_fn=print_fn)
        primary = f"{first} {last}"
    else:
        primary = ask("Value to search for", optional=False, input_fn=input_fn, print_fn=print_fn)
    refinements = {
        r: ask(_REFINEMENT_LABELS.get(r, r), input_fn=input_fn, print_fn=print_fn) for r in get_mode(mode).refinements
    }
    keyword = ask("Keyword (e.g. minecraft)", input_fn=input_fn, print_fn=print_fn)
    try:
        text = format_dorks(generate(mode, primary, refinements, keyword))
    except DorkintError as error:
        print_fn(f"Error: {error}")
        return None
    print_fn(f"\n{text}")
    return text


def _after_results(text: str, mode: str, input_fn: InputFn, print_fn: PrintFn) -> bool:
    """Results submenu; True = run another search in the same mode."""
    while True:
        choix = choose(
            "What now?",
            ["Save the links to a file", f"New search ({mode})"],
            back="Main menu",
            input_fn=input_fn,
            print_fn=print_fn,
        )
        if choix is None:
            return False
        if choix == 1:
            return True
        path = ask("Output file", optional=False, input_fn=input_fn, print_fn=print_fn)
        try:
            save(text + "\n", Path(path))
        except DorkintError as error:
            print_fn(f"Error: {error}")
        else:
            print_fn(f"Links saved to '{path}'.")


_CLEAR_SCREEN = "[2J[3J[H"


def _show_banner(print_fn: PrintFn) -> None:
    print_fn(_CLEAR_SCREEN + banner())


def run(input_fn: InputFn = input, print_fn: PrintFn = print) -> None:
    while (index := choose("Search mode", MODES, back="Quit", input_fn=input_fn, print_fn=print_fn)) is not None:
        mode = MODES[index]
        while (text := _search(mode, input_fn, print_fn)) is not None:
            if not _after_results(text, mode, input_fn, print_fn):
                break
        _show_banner(print_fn)
