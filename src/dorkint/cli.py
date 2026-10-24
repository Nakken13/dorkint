"""CLI entry point: one subcommand per search mode."""

import sys
from pathlib import Path
from typing import Annotated, NoReturn

import click
import typer
from typer.core import TyperGroup

from dorkint import __version__
from dorkint.banner import banner
from dorkint.builder import DorkintError, generate, get_mode
from dorkint.output import format_dorks, format_info, save
from dorkint.visual import render_html

MODES = ("fullname", "username", "city", "site", "email", "phone", "company")


class _ModeGroup(TyperGroup):
    """Root group: banner in the help, unknown-mode errors."""

    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(errors="replace")  # braille outside the console encoding: no crash
        typer.echo(typer.style(banner(), fg=typer.colors.CYAN))
        super().format_help(ctx, formatter)

    def resolve_command(
        self, ctx: click.Context, args: list[str]
    ) -> tuple[str | None, click.Command | None, list[str]]:
        name = args[0] if args else ""
        if name and not name.startswith("-") and self.get_command(ctx, name) is None:
            raise click.UsageError(
                f"Unknown mode: '{name}'. Available modes: {', '.join(MODES)}.", ctx
            )
        return super().resolve_command(ctx, args)


app = typer.Typer(
    cls=_ModeGroup,
    name="dorkint",
    help=(
        "Generates Google dorks for OSINT reconnaissance (no search is run). "
        "For authorized targets only: see DISCLAIMER.md."
    ),
    invoke_without_command=True,
    add_completion=False,
)


def _show_version(value: bool) -> None:
    if value:
        typer.echo(f"dorkint {__version__}")
        raise typer.Exit()


def _show_info(value: bool) -> None:
    if value:
        typer.echo(format_info([get_mode(m) for m in MODES]))
        raise typer.Exit()


@app.callback()
def _root(
    ctx: typer.Context,
    version: Annotated[
        bool, typer.Option("--version", callback=_show_version, is_eager=True, help="Show the version.")
    ] = False,
    info: Annotated[
        bool,
        typer.Option("--info", callback=_show_info, is_eager=True, help="List the dork patterns of each mode."),
    ] = False,
) -> None:
    """Without a mode, opens the interactive menu."""
    if ctx.invoked_subcommand is None:
        from dorkint.tui import main as tui_main

        tui_main()


def _fail(message: str) -> NoReturn:
    typer.echo(f"Error: {message}", err=True)
    raise typer.Exit(2)


def _register(mode: str) -> None:
    def command(
        words: Annotated[
            list[str] | None, typer.Argument(metavar="VALUE...", help="Value to search for (quotes optional).")
        ] = None,
        city: Annotated[str | None, typer.Option(help="Known city (refinement).")] = None,
        company: Annotated[str | None, typer.Option(help="Known company (refinement).")] = None,
        keyword: Annotated[str | None, typer.Option(help="Keyword added to every dork (e.g. minecraft).")] = None,
        out: Annotated[Path | None, typer.Option(help="File where the links are saved.")] = None,
        html: Annotated[Path | None, typer.Option(help="File where a visual HTML report (cards) is saved.")] = None,
        force: Annotated[bool, typer.Option("--force", help="Overwrite the --out/--html file if it exists.")] = False,
    ) -> None:
        if not words:
            _fail(f"missing primary value for mode '{mode}'.")
        try:
            groups = generate(mode, " ".join(words), {"city": city, "company": company}, keyword)
            text = format_dorks(groups)
            if out:
                save(text + "\n", out, overwrite=force)
            if html:
                save(render_html(groups, title=f"Dorkint: {mode} {' '.join(words)}"), html, overwrite=force)
        except DorkintError as error:
            _fail(str(error))
        typer.echo(text)
        if out:
            typer.echo(f"\nLinks saved to '{out}'.", err=True)
        if html:
            typer.echo(f"\nVisual report saved to '{html}'.", err=True)

    command.__doc__ = f"Mode '{mode}'."
    app.command(name=mode)(command)


for _mode in MODES:
    _register(_mode)


def main() -> None:
    app()
