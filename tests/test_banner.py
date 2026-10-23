from typer.testing import CliRunner

from dorkint.banner import banner
from dorkint.cli import app

runner = CliRunner()
TITRE = r" |___/\___/_| |_\_\_|_||_\__|"


def test_banner_fits_a_terminal() -> None:
    text = banner()
    assert max(len(line) for line in text.splitlines()) <= 80


def test_banner_has_an_eye_above_the_big_title() -> None:
    lines = banner().splitlines()
    assert len(lines) == 13
    assert "⣿" in lines[3]
    assert lines[-1].strip() == TITRE.strip()


def test_help_shows_banner() -> None:
    result = runner.invoke(app, ["--help"])
    assert TITRE in result.output


def test_results_and_version_have_no_banner() -> None:
    assert TITRE not in runner.invoke(app, ["--version"]).output
    assert TITRE not in runner.invoke(app, ["username", "jdupont"]).output
