import tomllib
from pathlib import Path

import pytest
from typer.testing import CliRunner

from dorkint import tui
from dorkint.cli import app

runner = CliRunner()


def test_main_refuses_without_tty(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("sys.stdin.isatty", lambda: False, raising=False)
    with pytest.raises(SystemExit) as exc:
        tui.main()
    assert exc.value.code == 2
    assert "dorkint" in capsys.readouterr().err


@pytest.mark.parametrize("error", [KeyboardInterrupt, EOFError])
def test_main_exits_cleanly_on_ctrl_c_or_eof(
    monkeypatch: pytest.MonkeyPatch, error: type[BaseException]
) -> None:
    monkeypatch.setattr("sys.stdin.isatty", lambda: True, raising=False)

    def boom(*_: object, **__: object) -> None:
        raise error

    monkeypatch.setattr("dorkint.tui.flow.run", boom)
    tui.main()  # raises nothing


def test_bare_dorkint_launches_menu(monkeypatch: pytest.MonkeyPatch) -> None:
    lance: list[bool] = []
    monkeypatch.setattr("dorkint.tui.main", lambda: lance.append(True))
    assert runner.invoke(app, []).exit_code == 0
    assert lance == [True]


def test_bare_dorkint_without_tty_points_to_flags_cli() -> None:
    result = runner.invoke(app, [])  # CliRunner : stdin non-tty
    assert result.exit_code == 2
    assert "dorkint <mode>" in result.output


def test_menu_subcommand_is_gone() -> None:
    result = runner.invoke(app, ["menu"])
    assert result.exit_code == 2
    assert "Unknown mode" in result.output


def test_dorkint_tool_script_declared() -> None:
    data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["scripts"]["dorkint-tool"] == "dorkint.tui:main"


def test_main_clears_screen_before_banner(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("sys.stdin.isatty", lambda: True, raising=False)
    monkeypatch.setattr("dorkint.tui.flow.run", lambda: None)
    tui.main()
    assert capsys.readouterr().out.startswith("\x1b[2J\x1b[3J\x1b[H")


def test_main_clears_screen_on_ctrl_c(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    def interrupt() -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr("sys.stdin.isatty", lambda: True, raising=False)
    monkeypatch.setattr("dorkint.tui.flow.run", interrupt)
    tui.main()
    assert capsys.readouterr().out.endswith("\x1b[2J\x1b[3J\x1b[H")
