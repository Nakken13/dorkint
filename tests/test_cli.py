import pytest
from typer.testing import CliRunner

import dorkint
from dorkint.cli import MODES, app

runner = CliRunner()


def test_seven_modes_declared() -> None:
    assert MODES == ("nom-prenom", "username", "ville", "site", "mail", "tel", "entreprise")


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert dorkint.__version__ in result.output


def test_help_lists_every_mode() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for mode in MODES:
        assert mode in result.output


def test_no_args_shows_help_and_fails() -> None:
    result = runner.invoke(app, [])
    assert result.exit_code != 0
    assert "Usage" in result.output


def test_unknown_mode_error_in_french() -> None:
    result = runner.invoke(app, ["inconnu", "x"])
    assert result.exit_code != 0
    assert "Mode inconnu" in result.output
    assert "inconnu" in result.output


@pytest.mark.parametrize("mode", MODES)
def test_missing_value_error_in_french(mode: str) -> None:
    result = runner.invoke(app, [mode])
    assert result.exit_code != 0
    assert "valeur" in result.output.lower()
    assert "manquant" in result.output.lower()


@pytest.mark.parametrize("mode", MODES)
def test_mode_accepts_value_and_refinements(mode: str) -> None:
    result = runner.invoke(
        app, [mode, "Jean Dupont", "--ville", "Lyon", "--entreprise", "Acme", "--out", "x.txt"]
    )
    assert result.exit_code == 0
    assert mode in result.output


def test_mode_help_documents_options() -> None:
    result = runner.invoke(app, ["nom-prenom", "--help"])
    assert result.exit_code == 0
    for option in ("--ville", "--entreprise", "--out"):
        assert option in result.output
