"""Point d'entrée CLI : un sous-commande par mode de recherche."""

from pathlib import Path
from typing import Annotated, NoReturn

import click
import typer
from typer.core import TyperGroup

from dorkint import __version__
from dorkint.builder import DorkintError, generer
from dorkint.output import formater, sauvegarder

MODES = ("nom-prenom", "username", "ville", "site", "mail", "tel", "entreprise")


class _ModeGroup(TyperGroup):
    """Groupe dont les erreurs de mode inconnu sont en français."""

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
    help="Génère des Google dorks pour la reconnaissance OSINT (aucune recherche exécutée).",
    no_args_is_help=True,
    add_completion=False,
)


def _show_version(value: bool) -> None:
    if value:
        typer.echo(f"dorkint {__version__}")
        raise typer.Exit()


@app.callback()
def _root(
    version: Annotated[
        bool, typer.Option("--version", callback=_show_version, is_eager=True, help="Affiche la version.")
    ] = False,
) -> None:
    """Options globales."""


def _fail(message: str) -> NoReturn:
    typer.echo(f"Erreur : {message}", err=True)
    raise typer.Exit(2)


def _register(mode: str) -> None:
    def command(
        valeur: Annotated[str | None, typer.Argument(help="Valeur principale à rechercher.")] = None,
        ville: Annotated[str | None, typer.Option(help="Ville connue (affinage).")] = None,
        entreprise: Annotated[str | None, typer.Option(help="Entreprise connue (affinage).")] = None,
        out: Annotated[Path | None, typer.Option(help="Fichier où sauvegarder les liens.")] = None,
        force: Annotated[bool, typer.Option("--force", help="Écrase le fichier --out s'il existe.")] = False,
    ) -> None:
        if valeur is None:
            _fail(f"valeur principale manquante pour le mode '{mode}'.")
        try:
            groupes = generer(mode, valeur, {"ville": ville, "entreprise": entreprise})
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
