from pathlib import Path

import pytest

from dorkint.builder import DorkintError
from dorkint.output import format_dorks, save, to_google_url

BASE = "https://www.google.com/search?q="


@pytest.mark.parametrize(
    ("query", "attendu"),
    [
        ("jean dupont", "jean+dupont"),
        ('"Jean Dupont"', "%22Jean+Dupont%22"),
        ("site:linkedin.com/in", "site%3Alinkedin.com%2Fin"),
        ("a&b=c", "a%26b%3Dc"),
        ("Hélène Müller", "H%C3%A9l%C3%A8ne+M%C3%BCller"),
        ("a OR b -c", "a+OR+b+-c"),
    ],
)
def test_vers_url_google_encodes(query: str, attendu: str) -> None:
    assert to_google_url(query) == BASE + attendu


def test_format_dorks_groups_by_category_with_one_url_per_line() -> None:
    groups = {
        "Networks": ["site:x.com a", "site:y.com a"],
        "Press": ["a presse"],
    }
    lines = format_dorks(groups).splitlines()
    assert lines[0] == "## Networks"
    assert lines[1] == to_google_url("site:x.com a")
    assert lines[2] == to_google_url("site:y.com a")
    assert "## Press" in lines
    assert all(l.startswith(("##", BASE)) or not l for l in lines)


def test_format_dorks_empty() -> None:
    assert format_dorks({}) == ""


def test_save_writes_utf8(tmp_path: Path) -> None:
    target = tmp_path / "liens.txt"
    save("é\n", target)
    assert target.read_text(encoding="utf-8") == "é\n"


def test_save_refuses_overwrite_without_flag(tmp_path: Path) -> None:
    target = tmp_path / "liens.txt"
    target.write_text("ancien", encoding="utf-8")
    with pytest.raises(DorkintError, match="already exists"):
        save("nouveau", target)
    assert target.read_text(encoding="utf-8") == "ancien"
    save("nouveau", target, overwrite=True)
    assert target.read_text(encoding="utf-8") == "nouveau"


def test_save_invalid_path(tmp_path: Path) -> None:
    with pytest.raises(DorkintError, match="Cannot write"):
        save("x", tmp_path / "absent" / "liens.txt")
    with pytest.raises(DorkintError, match="Cannot write"):
        save("x", tmp_path, overwrite=True)
