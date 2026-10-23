"""Point d'entrée CLI : un sous-commande par mode de recherche."""

from pathlib import Path
from typing import Annotated, NoReturn

import click
import typer
from typer.core import TyperGroup

from dorkint import __version__
from dorkint.banner import banner
from dorkint.builder import DorkintError, generer, get_mode
from dorkint.output import formater, formater_info, sauvegarder

MODES = ("fullname", "username", "city", "site", "email", "phone", "company")


class _ModeGroup(TyperGroup):
    """Groupe racine : bannière dans l'aide, erreurs de mode inconnu en français."""

    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        typer.echo(typer.style(banner(), fg=typer.colors.CYAN))
        super().format_help(ctx, formatter)

    def resolve_command(
        self, ctx: click.Context, args: list[str]
    ) -> tuple[str | None, click.Command | None, list[str]]:
        name = args[0] if args else ""
        if name and not name.startswith("-") and self.get_command(ctx, name) is None:
            raise click.UsageError(
                f"Mode inconnu : '{name}'. Modes disponibles : {', '.join(MODES)}.", ctx
            )
        return super().resolve_command(ctx, args)


app = typer.Typer(
    cls=_ModeGroup,
    name="dorkint",
    help=(
        "Génère des Google dorks pour la reconnaissance OSINT (aucune recherche exécutée). "
        "Usage réservé à des cibles autorisées : voir DISCLAIMER.md."
    ),
    no_args_is_help=True,
    add_completion=False,
)


def _show_version(value: bool) -> None:
    if value:
        typer.echo(f"dorkint {__version__}")
        raise typer.Exit()


def _show_info(value: bool) -> None:
    if value:
        typer.echo(formater_info([get_mode(m) for m in MODES]))
        raise typer.Exit()


@app.callback()
def _root(
    version: Annotated[
        bool, typer.Option("--version", callback=_show_version, is_eager=True, help="Affiche la version.")
    ] = False,
    info: Annotated[
        bool,
        typer.Option("--info", callback=_show_info, is_eager=True, help="Liste les dorks (patrons) de chaque mode."),
    ] = False,
) -> None:
    """Options globales."""


def _fail(message: str) -> NoReturn:
    typer.echo(f"Erreur : {message}", err=True)
    raise typer.Exit(2)


def _register(mode: str) -> None:
    def command(
        words: Annotated[
            list[str] | None, typer.Argument(metavar="VALUE...", help="Valeur à rechercher (guillemets facultatifs).")
        ] = None,
        city: Annotated[str | None, typer.Option(help="Ville connue (affinage).")] = None,
        company: Annotated[str | None, typer.Option(help="Entreprise connue (affinage).")] = None,
        out: Annotated[Path | None, typer.Option(help="Fichier où sauvegarder les liens.")] = None,
        force: Annotated[bool, typer.Option("--force", help="Écrase le fichier --out s'il existe.")] = False,
    ) -> None:
        if not words:
            _fail(f"valeur principale manquante pour le mode '{mode}'.")
        try:
            groupes = generer(mode, " ".join(words), {"city": city, "company": company})
            texte = formater(groupes)
            if out:
                sauvegarder(texte + "\n", out, ecraser=force)
        except DorkintError as erreur:
            _fail(str(erreur))
        typer.echo(texte)
        if out:
            typer.echo(f"\nLiens sauvegardés dans '{out}'.", err=True)

    command.__doc__ = f"Mode « {mode} »."
    app.command(name=mode)(command)


for _mode in MODES:
    _register(_mode)


def main() -> None:
    app()
