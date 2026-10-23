from pathlib import Path

import pytest

from dorkint.builder import Dork, DorkintError
from dorkint.output import formater, sauvegarder, vers_url_google

BASE = "https://www.google.com/search?q="


@pytest.mark.parametrize(
    ("requete", "attendu"),
    [
        ("jean dupont", "jean+dupont"),
        ('"Jean Dupont"', "%22Jean+Dupont%22"),
        ("site:linkedin.com/in", "site%3Alinkedin.com%2Fin"),
        ("a&b=c", "a%26b%3Dc"),
        ("Hélène Müller", "H%C3%A9l%C3%A8ne+M%C3%BCller"),
        ("a OR b -c", "a+OR+b+-c"),
    ],
)
def test_vers_url_google_encodes(requete: str, attendu: str) -> None:
    assert vers_url_google(requete) == BASE + attendu


def test_formater_groups_by_category_with_one_url_per_line() -> None:
    groupes = {
        "Réseaux": [Dork("Réseaux", "site:x.com a"), Dork("Réseaux", "site:y.com a")],
        "Presse": [Dork("Presse", "a presse")],
    }
    lignes = formater(groupes).splitlines()
    assert lignes[0] == "## Réseaux"
    assert lignes[1] == vers_url_google("site:x.com a")
    assert lignes[2] == vers_url_google("site:y.com a")
    assert "## Presse" in lignes
    assert all(l.startswith(("##", BASE)) or not l for l in lignes)


def test_formater_empty() -> None:
    assert formater({}) == ""


def test_sauvegarder_writes_utf8(tmp_path: Path) -> None:
    cible = tmp_path / "liens.txt"
    sauvegarder("é\n", cible)
    assert cible.read_text(encoding="utf-8") == "é\n"


def test_sauvegarder_refuses_overwrite_without_flag(tmp_path: Path) -> None:
    cible = tmp_path / "liens.txt"
    cible.write_text("ancien", encoding="utf-8")
    with pytest.raises(DorkintError, match="existe déjà"):
        sauvegarder("nouveau", cible)
    assert cible.read_text(encoding="utf-8") == "ancien"
    sauvegarder("nouveau", cible, ecraser=True)
    assert cible.read_text(encoding="utf-8") == "nouveau"


def test_sauvegarder_invalid_path(tmp_path: Path) -> None:
    with pytest.raises(DorkintError, match="Impossible"):
        sauvegarder("x", tmp_path / "absent" / "liens.txt")
    with pytest.raises(DorkintError, match="Impossible"):
        sauvegarder("x", tmp_path, ecraser=True)
