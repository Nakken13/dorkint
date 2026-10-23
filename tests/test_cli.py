from pathlib import Path

import pytest
from typer.testing import CliRunner

import dorkint
from dorkint.cli import MODES, app

runner = CliRunner()


def test_seven_modes_declared() -> None:
    assert MODES == ("fullname", "username", "city", "site", "email", "phone", "company")


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


def test_registered_modes_match_cli_modes() -> None:
    from dorkint import builder

    builder.load_modes()
    assert set(builder._REGISTRY) == set(MODES)


@pytest.mark.parametrize("mode", MODES)
def test_mode_prints_clickable_google_links_by_category(mode: str) -> None:
    result = runner.invoke(app, [mode, "exemple.fr" if mode == "site" else "Jean Dupont"])
    assert result.exit_code == 0
    assert "## " in result.output
    assert "https://www.google.com/search?q=" in result.output


def test_refinement_adds_links() -> None:
    sans = runner.invoke(app, ["fullname", "Jean Dupont"]).output
    avec = runner.invoke(app, ["fullname", "Jean Dupont", "--city", "Lyon"]).output
    assert avec.count("https://") > sans.count("https://")
    assert "Lyon" in avec


def test_unsupported_refinement_is_a_clean_error() -> None:
    result = runner.invoke(app, ["city", "Lyon", "--city", "Paris"])
    assert result.exit_code == 2
    assert "affinage" in result.output


def test_out_saves_links_and_refuses_to_overwrite(tmp_path: Path) -> None:
    cible = tmp_path / "liens.txt"
    result = runner.invoke(app, ["username", "jdupont", "--out", str(cible)])
    assert result.exit_code == 0
    assert "https://www.google.com/search?q=" in cible.read_text(encoding="utf-8")
    again = runner.invoke(app, ["username", "jdupont", "--out", str(cible)])
    assert again.exit_code == 2
    assert "existe déjà" in again.output
    forced = runner.invoke(app, ["username", "jdupont", "--out", str(cible), "--force"])
    assert forced.exit_code == 0


def test_out_invalid_path_is_a_clean_error(tmp_path: Path) -> None:
    result = runner.invoke(app, ["username", "jdupont", "--out", str(tmp_path / "x" / "y.txt")])
    assert result.exit_code == 2
    assert "Impossible" in result.output


def test_blank_value_is_rejected() -> None:
    result = runner.invoke(app, ["username", "   "])
    assert result.exit_code == 2


def test_mode_help_documents_options() -> None:
    result = runner.invoke(app, ["fullname", "--help"])
    assert result.exit_code == 0
    for option in ("--city", "--company", "--out", "--force"):
        assert option in result.output
