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


def test_info_lists_every_mode_category_and_pattern() -> None:
    from dorkint import builder

    result = runner.invoke(app, ["--info"])
    assert result.exit_code == 0
    for mode in MODES:
        assert f"# {mode}" in result.output
    for mode in MODES:
        for category in builder.get_mode(mode).categories:
            assert f"## {category.name}" in result.output
            for template in category.templates:
                assert template.pattern in result.output
    assert "https://" not in result.output


def test_info_flags_templates_needing_refinements() -> None:
    result = runner.invoke(app, ["--info"])
    assert "{primary} {city}  [--city]" in result.output
    assert "{local} site:{domain:raw}  [local, domain]" in result.output


def test_help_lists_every_mode() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for mode in MODES:
        assert mode in result.output


def test_unknown_mode_error() -> None:
    result = runner.invoke(app, ["unknown", "x"])
    assert result.exit_code != 0
    assert "Unknown mode" in result.output
    assert "unknown" in result.output


@pytest.mark.parametrize("mode", MODES)
def test_missing_value_error(mode: str) -> None:
    result = runner.invoke(app, [mode])
    assert result.exit_code != 0
    assert "value" in result.output.lower()
    assert "missing" in result.output.lower()


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
    without_city = runner.invoke(app, ["fullname", "Jean Dupont"]).output
    with_city = runner.invoke(app, ["fullname", "Jean Dupont", "--city", "Lyon"]).output
    assert with_city.count("https://") > without_city.count("https://")
    assert "Lyon" in with_city


def test_unsupported_refinement_is_a_clean_error() -> None:
    result = runner.invoke(app, ["city", "Lyon", "--city", "Paris"])
    assert result.exit_code == 2
    assert "refinement" in result.output


def test_out_saves_links_and_refuses_to_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "liens.txt"
    result = runner.invoke(app, ["username", "jdupont", "--out", str(target)])
    assert result.exit_code == 0
    assert "https://www.google.com/search?q=" in target.read_text(encoding="utf-8")
    again = runner.invoke(app, ["username", "jdupont", "--out", str(target)])
    assert again.exit_code == 2
    assert "already exists" in again.output
    forced = runner.invoke(app, ["username", "jdupont", "--out", str(target), "--force"])
    assert forced.exit_code == 0


def test_out_invalid_path_is_a_clean_error(tmp_path: Path) -> None:
    result = runner.invoke(app, ["username", "jdupont", "--out", str(tmp_path / "x" / "y.txt")])
    assert result.exit_code == 2
    assert "Cannot write" in result.output


def test_blank_value_is_rejected() -> None:
    result = runner.invoke(app, ["username", "   "])
    assert result.exit_code == 2


def test_mode_help_documents_options() -> None:
    result = runner.invoke(app, ["fullname", "--help"])
    assert result.exit_code == 0
    for option in ("--city", "--company", "--out", "--force"):
        assert option in result.output


def test_multiple_words_without_quotes_are_joined() -> None:
    sans_guillemets = runner.invoke(app, ["fullname", "john", "doe"])
    avec_guillemets = runner.invoke(app, ["fullname", "john doe"])
    assert sans_guillemets.exit_code == 0
    assert sans_guillemets.output == avec_guillemets.output
    assert "%22john+doe%22" in sans_guillemets.output


def test_options_still_work_after_unquoted_words() -> None:
    result = runner.invoke(app, ["fullname", "john", "doe", "--city", "Lyon"])
    assert result.exit_code == 0
    assert "%22john+doe%22+%22Lyon%22" in result.output


def test_keyword_option_is_appended_to_every_dork() -> None:
    result = runner.invoke(app, ["username", "kalira", "--keyword", "minecraft"])
    assert result.exit_code == 0
    dorks = [l.strip() for l in result.output.splitlines() if "kalira" in l]
    assert dorks and all(l.endswith('%22minecraft%22') for l in dorks)


def test_keyword_forbidden_term_exits_2() -> None:
    result = runner.invoke(app, ["username", "kalira", "--keyword", "password"])
    assert result.exit_code == 2
