"""Bannière ASCII (un oeil et le nom en gros) affichée dans l'aide."""

_EYE = (
    r"          .--------------.",
    r"      .-''   .--------.   ''-.",
    r"   .-'      /  .----.  \      '-.",
    r"  <        |  ( (  ) )  |        >",
    r"   '-.      \  '----'  /      .-'",
    r"      '-..   '--------'   ..-'",
    r"          '--------------'",
)

_BS = chr(92)  # antislash, hors littéral pour éviter les échappements

# Police "standard" de figlet, une lettre par bloc de 5 lignes.
_LETTERS = {
    "D": (r" ____  ", r"|  _ \ ", r"| | | |", r"| |_| |", r"|____/ "),
    "O": (r"  ___  ", r" / _ \ ", r"| | | |", r"| |_| |", r" \___/ "),
    "R": (r" ____  ", r"|  _ \ ", r"| |_) |", r"|  _ < ", "|_| " + _BS + "_" + _BS),
    "K": (r" _  __", r"| |/ /", r"| ' / ", r"| . \ ", "|_|" + _BS + "_" + _BS),
    "I": (r" ___ ", r"|_ _|", r" | | ", r" | | ", r"|___|"),
    "N": (r" _   _ ", r"| \ | |", r"|  \| |", r"| |\  |", r"|_| \_|"),
    "T": (r" _____ ", r"|_   _|", r"  | |  ", r"  | |  ", r"  |_|  "),
}


def _big(word: str) -> str:
    return "\n".join("".join(_LETTERS[c][row] for c in word) for row in range(5))


def banner() -> str:
    """Oeil puis `DORKINT` en gros, centrés sur la largeur du titre."""
    title = _big("DORKINT")
    largeur = max(len(ligne) for ligne in title.splitlines())
    eye_largeur = max(len(ligne) for ligne in _EYE)
    decalage = " " * max((largeur - eye_largeur) // 2, 0)
    eye = "\n".join(decalage + ligne for ligne in _EYE)
    return f"{eye}\n{title}\n"
