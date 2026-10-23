"""Bannière (un oeil en braille et le nom `Dorkint`) affichée dans l'aide."""

import shutil

_EYE = (
    "⠀              ⣀⣀⣀⡀⢰⠆⠂⠄⡀⠀⠀⠀⠀⠀⠀",
    "⠁⠀⠀⠀⠀⠀⠈⢀⢠⠴⠒⢿⣉⣦⣱⡇⣧⢼⣯⣿⠲⣥⣀⡀⠁⠠⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⡀⢎⠰⣈⣵⣾⣿⣿⣿⣿⣿⣿⣿⣷⣿⣷⣯⡴⢆⡤⠀⡄⠀⠀",
    "⠀⠀⠀⠀⡀⢆⠱⣨⣶⠿⣿⠟⠋⣿⣿⣿⣿⣿⣿⣯⠛⠿⣿⣿⣷⣒⣩⠄⠀⠀",
    "⠀⠀⠐⠊⡴⢬⡾⠛⠁⠀⣿⣷⣼⣿⣿⣿⣿⣿⣿⣿⠀⠀⢈⠛⣻⡶⠶⠗⠂⠀",
    "⠀⠀⠐⢀⣴⠛⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⡠⢀⣴⡿⠉⠡⠀⠀⠀",
    "⠀⠈⠀⠺⠕⠒⠂⠀⡀⠀⠀⠈⠙⠛⠻⠛⡛⠋⠀⠀⣠⣶⣿⠿⡣⠐⠀⠀⠀⠀",
    "⠃⢀⠀⠀⠀⠀⠀⠀⠐⠀⠠⢠⡴⢦⣤⣄⣶⡶⣾⢿⠛⠟⠂⠓⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠈⠐⠀⠄⢀⠀⠀⠀⠒⠁⠊⠉⡇⢛⠾⠑⠁⠉⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀",
)

_TITLE = (
    r"  ___          _   _     _   ",
    r" |   \ ___ _ _| |_(_)_ _| |_ ",
    r" | |) / _ \ '_| / / | ' \  _|",
    r" |___/\___/_| |_\_\_|_||_\__|",
)


def banner() -> str:
    """Oeil puis `Dorkint`, centrés l'un sur l'autre."""
    eye_largeur = max(len(ligne) for ligne in _EYE)
    titre_largeur = max(len(ligne) for ligne in _TITLE)
    terminal = shutil.get_terminal_size((80, 24)).columns
    lignes = [ligne.ljust(eye_largeur).center(terminal).rstrip() for ligne in _EYE]
    lignes += [ligne.ljust(titre_largeur).center(terminal).rstrip() for ligne in _TITLE]
    return "\n".join(lignes) + "\n"
