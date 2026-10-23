"""Banner (a braille eye and the name `Dorkint`) shown in the help."""

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
    """Eye then `Dorkint`, each centered on the terminal."""
    eye_width = max(len(line) for line in _EYE)
    title_width = max(len(line) for line in _TITLE)
    terminal = shutil.get_terminal_size((80, 24)).columns
    lines = [line.ljust(eye_width).center(terminal).rstrip() for line in _EYE]
    lines += [line.ljust(title_width).center(terminal).rstrip() for line in _TITLE]
    return "\n".join(lines) + "\n"
