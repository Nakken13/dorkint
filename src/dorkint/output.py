"""Sortie : dorks -> URL Google cliquables, affichage groupé, sauvegarde fichier."""

from collections.abc import Mapping, Sequence
from pathlib import Path
from urllib.parse import quote_plus

from dorkint.builder import Dork, DorkintError, Mode

_GOOGLE = "https://www.google.com/search?q="


def vers_url_google(requete: str) -> str:
    return _GOOGLE + quote_plus(requete)


def formater(groupes: Mapping[str, Sequence[Dork]]) -> str:
    """Une URL par ligne sous un en-tête `## Catégorie` (rien qui casse le ctrl+clic)."""
    blocs = [
        "\n".join([f"## {categorie}", *(vers_url_google(d.query) for d in dorks)])
        for categorie, dorks in groupes.items()
    ]
    return "\n\n".join(blocs)


def formater_info(modes: Sequence[Mode]) -> str:
    """Patrons bruts de chaque mode ; `[...]` = affinages (`--x`) ou valeurs dérivées requis."""
    blocs = []
    for mode in modes:
        lignes = [f"# {mode.name}"]
        for categorie in mode.categories:
            lignes.append(f"## {categorie.name}")
            for t in categorie.templates:
                requis = ", ".join(f"--{r}" if r in mode.refinements else r for r in t.requires)
                lignes.append(f"{t.pattern}  [{requis}]" if requis else t.pattern)
        blocs.append("\n".join(lignes))
    return "\n\n".join(blocs)


def sauvegarder(texte: str, chemin: Path, ecraser: bool = False) -> None:
    if chemin.exists() and not ecraser:
        raise DorkintError(f"Le fichier '{chemin}' existe déjà (utiliser --force pour l'écraser).")
    try:
        chemin.write_text(texte, encoding="utf-8")
    except OSError as erreur:
        raise DorkintError(f"Impossible d'écrire '{chemin}' : {erreur.strerror}.") from erreur
