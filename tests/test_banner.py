from typer.testing import CliRunner

from dorkint.banner import banner
from dorkint.cli import app

runner = CliRunner()
TITRE = r"|  _ \  / _ \ |  _ \ | |/ /|_ _|| \ | ||_   _|"


def test_banner_is_pure_ascii_and_fits_a_terminal() -> None:
    texte = banner()
    assert texte.isascii()
    assert max(len(ligne) for ligne in texte.splitlines()) <= 80


def test_banner_has_an_eye_above_the_big_title() -> None:
    lignes = banner().splitlines()
    assert len(lignes) == 12
    assert "( (  ) )" in lignes[3]
    assert lignes[-4] == TITRE


def test_help_shows_banner() -> None:
    result = runner.invoke(app, ["--help"])
    assert TITRE in result.output


def test_no_args_shows_banner() -> None:
    result = runner.invoke(app, [])
    assert TITRE in result.output


def test_results_and_version_have_no_banner() -> None:
    assert TITRE not in runner.invoke(app, ["--version"]).output
    assert TITRE not in runner.invoke(app, ["username", "jdupont"]).output
