"""Menu flow: mode -> value -> refinements -> keyword -> results. No direct I/O."""

import sys
import tempfile
import webbrowser
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import NamedTuple

from dorkint.banner import banner
from dorkint.builder import DorkintError, generate, refinements_of
from dorkint.modes import MODES, dork_counts
from dorkint.output import format_dorks, save
from dorkint.tui.prompts import InputFn, PrintFn, ask, choose
from dorkint.visual import render_cards, render_html, render_info

OpenFn = Callable[[str], object]


class _Results(NamedTuple):
    text: str
    groups: Mapping[str, Sequence[str]]
    title: str


_ABOUT = (
    "Dorkint automates the writing of Google dorks for OSINT reconnaissance.",
    "Pick a mode, give it a target, and get ready-made queries grouped by category.",
    "It never scrapes or runs a search: you open the links yourself.",
    "Only use it on targets you are authorized to look into.",
)

def _stats() -> tuple[str, ...]:
    counts = dork_counts()
    per_mode = ", ".join(f"{name} {n}" for name, n in counts.items())
    return ("", "Stats", f"{sum(counts.values())} dorks across {len(counts)} modes", per_mode)


_REFINEMENT_LABELS = {"city": "Known city", "company": "Known company"}


def _search(mode: str, input_fn: InputFn, print_fn: PrintFn) -> _Results | None:
    """Asks the mode's questions; returns the results, or None if an error was shown."""
    if mode == "fullname":
        first = ask("First name", optional=False, input_fn=input_fn, print_fn=print_fn)
        last = ask("Last name", optional=False, input_fn=input_fn, print_fn=print_fn)
        primary = f"{first} {last}"
    else:
        primary = ask("Value to search for", optional=False, input_fn=input_fn, print_fn=print_fn)
    refinements = {
        r: ask(_REFINEMENT_LABELS.get(r, r), input_fn=input_fn, print_fn=print_fn) for r in refinements_of(mode)
    }
    keyword = ask("Keyword (e.g. minecraft)", input_fn=input_fn, print_fn=print_fn)
    try:
        groups = generate(mode, primary, refinements, keyword)
    except DorkintError as error:
        print_fn(f"Error: {error}")
        return None
    print_fn("\n" + render_cards(groups, color=sys.stdout.isatty()))
    return _Results(format_dorks(groups), groups, f"Dorkint: {mode} {primary}")


def _open_report(results: _Results, open_fn: OpenFn) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".html", prefix="dorkint-", delete=False, encoding="utf-8") as f:
        f.write(render_html(results.groups, title=results.title))
    open_fn(Path(f.name).as_uri())


def _after_results(results: _Results, mode: str, input_fn: InputFn, print_fn: PrintFn, open_fn: OpenFn) -> bool:
    """Results submenu; True = run another search in the same mode."""
    while True:
        choix = choose(
            "What now?",
            ["Save the links to a file", f"New search ({mode})", "Open the visual report in the browser"],
            back="Main menu",
            input_fn=input_fn,
            print_fn=print_fn,
        )
        if choix is None:
            return False
        if choix == 1:
            return True
        if choix == 2:
            _open_report(results, open_fn)
            print_fn("Visual report opened in the browser.")
            continue
        path = ask("Output file", optional=False, input_fn=input_fn, print_fn=print_fn)
        try:
            save(results.text + "\n", Path(path))
        except DorkintError as error:
            print_fn(f"Error: {error}")
        else:
            print_fn(f"Links saved to '{path}'.")


_CLEAR_SCREEN = "\x1b[2J\x1b[3J\x1b[H"


def show_banner(print_fn: PrintFn) -> None:
    print_fn(_CLEAR_SCREEN + "\n" + banner().rstrip("\n"))  # the menu adds its own leading blank line


def run(input_fn: InputFn = input, print_fn: PrintFn = print, open_fn: OpenFn = webbrowser.open) -> None:
    modes = list(MODES)
    def show_about() -> None:
        print_fn("\n" + render_info("About dorkint", (*_ABOUT, *_stats()), color=sys.stdout.isatty()))

    while (
        index := choose(
            "Search mode", modes, columns=3, back="Quit", on_info=show_about, input_fn=input_fn, print_fn=print_fn
        )
    ) is not None:
        mode = list(MODES)[index]
        while (results := _search(mode, input_fn, print_fn)) is not None:
            if not _after_results(results, mode, input_fn, print_fn, open_fn):
                break
        show_banner(print_fn)
