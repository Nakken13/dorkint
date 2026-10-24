from collections.abc import Callable, Iterator

from dorkint.tui.prompts import ask, choose


def _scripted(*answers: str) -> tuple[Callable[[str], str], list[str]]:
    it: Iterator[str] = iter(answers)
    shown: list[str] = []

    def input_fn(prompt: str = "") -> str:
        shown.append(prompt)
        return next(it)

    return input_fn, shown


def test_choose_returns_zero_based_index() -> None:
    input_fn, _ = _scripted("2")
    assert choose("Mode", ["a", "b", "c"], input_fn=input_fn, print_fn=lambda *_: None) == 1


def test_choose_zero_means_back() -> None:
    input_fn, _ = _scripted("q")
    assert choose("Mode", ["a", "b"], input_fn=input_fn, print_fn=lambda *_: None) is None


def test_choose_reprompts_on_invalid_input() -> None:
    input_fn, shown = _scripted("x", "9", "", "1")
    out: list[str] = []
    assert choose("Mode", ["a", "b"], input_fn=input_fn, print_fn=out.append) == 0
    assert len(shown) == 4
    assert any("invalid" in line.lower() for line in out)


def test_choose_lists_numbered_options_and_back_label() -> None:
    input_fn, _ = _scripted("q")
    out: list[str] = []
    choose("Mode", ["alpha", "beta"], input_fn=input_fn, print_fn=out.append, back="Quit")
    text = "\n".join(out)
    assert "[1]" in text and "alpha" in text and "[2]" in text and "beta" in text
    assert "[q]" in text and "Quit" in text


def test_ask_enter_gives_empty_string() -> None:
    input_fn, _ = _scripted("")
    assert ask("Ville", input_fn=input_fn, print_fn=lambda *_: None) == ""


def test_ask_strips_value() -> None:
    input_fn, _ = _scripted("  Lyon ")
    assert ask("Ville", input_fn=input_fn, print_fn=lambda *_: None) == "Lyon"


def test_ask_required_reprompts_until_filled() -> None:
    input_fn, shown = _scripted("", "  ", "Jean")
    assert ask("Valeur", optional=False, input_fn=input_fn, print_fn=lambda *_: None) == "Jean"
    assert len(shown) == 3
