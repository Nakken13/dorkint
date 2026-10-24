import re
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import url2pathname

from dorkint.cli import MODES
from dorkint.tui.flow import run


def _run(*answers: str, open_fn=None) -> tuple[str, int]:
    """Plays the input script; returns (output, number of inputs consumed)."""
    it: Iterator[str] = iter(answers)
    out: list[str] = []
    consumed = 0

    def input_fn(prompt: str = "") -> str:
        nonlocal consumed
        out.append(prompt)
        consumed += 1
        return next(it)

    run(input_fn=input_fn, print_fn=out.append, open_fn=open_fn or (lambda url: None))
    return "\n".join(out), consumed


def _n(mode: str) -> str:
    return str(list(MODES).index(mode) + 1)


def test_quit_from_main_menu() -> None:
    text, consumed = _run("q")
    assert consumed == 1
    for mode in MODES:
        assert mode in text


def test_username_with_keyword_prints_dorks_with_keyword() -> None:
    text, _ = _run(_n("username"), "kalira", "", "", "minecraft", "q", "q")
    assert "kalira" in text and '"minecraft"' in text
    assert "google.com" not in text  # links are hidden behind labels


def test_enter_skips_every_optional_field() -> None:
    text, _ = _run(_n("username"), "kalira", "", "", "", "q", "q")
    assert "kalira" in text
    assert '"minecraft"' not in text


def test_refinements_come_from_the_mode() -> None:
    # city: a single refinement (company) -> menu, primary, company, keyword, results, menu = 6 inputs
    _, consumed = _run(_n("city"), "Lyon", "", "", "q", "q")
    assert consumed == 6
    # username: 2 refinements -> one more input
    _, consumed = _run(_n("username"), "kalira", "", "", "", "q", "q")
    assert consumed == 7


def test_refinement_value_crosses_into_dorks() -> None:
    text, _ = _run(_n("username"), "kalira", "Lyon", "", "", "q", "q")
    assert "Lyon" in text


def test_new_search_same_mode_reuses_mode() -> None:
    text, _ = _run(_n("city"), "Lyon", "", "", "2", "Paris", "", "", "q", "q")
    assert "Lyon" in text and "Paris" in text


def test_save_writes_file(tmp_path: Path) -> None:
    target = tmp_path / "liens.txt"
    _run(_n("username"), "kalira", "", "", "", "1", str(target), "q", "q")
    assert "google.com/search" in target.read_text(encoding="utf-8")


def test_save_refuses_to_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "liens.txt"
    target.write_text("ancien", encoding="utf-8")
    text, _ = _run(_n("username"), "kalira", "", "", "", "1", str(target), "q", "q")
    assert target.read_text(encoding="utf-8") == "ancien"
    assert "already exists" in text


def test_forbidden_keyword_shows_error_and_returns_to_menu() -> None:
    text, _ = _run(_n("username"), "kalira", "", "", "password", "q")
    assert "forbidden" in text


def test_fullname_asks_first_name_then_last_name() -> None:
    text, consumed = _run(_n("fullname"), "Jean", "Dupont", "", "", "", "q", "q")
    assert "First name" in text and "Last name" in text
    assert consumed == 8
    assert "Jean Dupont" in text


def test_visual_report_opens_html_in_browser() -> None:
    opened: list[str] = []
    _run(_n("username"), "kalira", "", "", "", "3", "q", "q", open_fn=opened.append)
    assert len(opened) == 1 and opened[0].endswith(".html")
    assert Path(url2pathname(urlparse(opened[0]).path)).read_text(encoding="utf-8").startswith("<!doctype html>")


def test_results_are_grouped_in_category_cards() -> None:
    text, _ = _run(_n("username"), "kalira", "", "", "", "q", "q")
    assert re.search(r"\(\d+\)", text)  # "<category> (<count>)" card titles
