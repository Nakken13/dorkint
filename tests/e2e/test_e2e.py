"""Tests de bout en bout : vrai processus `python -m dorkint`, réseau interdit."""

import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

SRC = Path(__file__).resolve().parents[2] / "src"
# Lance dorkint après avoir fait échouer toute connexion réseau.
NO_NETWORK = (
    "import socket, runpy, sys\n"
    "def _blocked(*a, **k): raise RuntimeError('acces reseau interdit')\n"
    "socket.socket.connect = _blocked\n"
    "socket.create_connection = _blocked\n"
    "sys.argv[0] = 'dorkint'\n"
    "runpy.run_module('dorkint', run_name='__main__')\n"
)
VALEURS = {
    "nom-prenom": "Jean Dupont",
    "username": "jdupont",
    "ville": "Lyon",
    "site": "exemple.fr",
    "mail": "jean.dupont@exemple.fr",
    "tel": "06 12 34 56 78",
    "entreprise": "Acme",
}


def lancer(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PYTHONPATH": str(SRC), "PYTHONIOENCODING": "utf-8"}
    return subprocess.run(
        [sys.executable, "-c", NO_NETWORK, *args],
        capture_output=True, text=True, encoding="utf-8", env=env, cwd=cwd, timeout=60, check=False,
    )


def urls(sortie: str) -> list[str]:
    return [ligne for ligne in sortie.splitlines() if ligne.startswith("http")]


@pytest.mark.parametrize(("mode", "valeur"), VALEURS.items())
def test_mode_outputs_decodable_google_urls(mode: str, valeur: str) -> None:
    result = lancer(mode, valeur)
    assert result.returncode == 0, result.stderr
    liens = urls(result.stdout)
    assert liens
    for lien in liens:
        parsed = urlparse(lien)
        assert (parsed.scheme, parsed.netloc, parsed.path) == ("https", "www.google.com", "/search")
        assert parse_qs(parsed.query)["q"][0].strip()
    requetes = [parse_qs(urlparse(l).query)["q"][0] for l in liens]
    cle = valeur if mode == "site" else f'"{valeur}"'
    assert any(cle in q for q in requetes)


def test_refinements_cross_variants() -> None:
    base = urls(lancer("nom-prenom", "Jean Dupont").stdout)
    affine = urls(lancer("nom-prenom", "Jean Dupont", "--ville", "Lyon", "--entreprise", "Acme").stdout)
    assert len(affine) > len(base)
    assert any("%22Lyon%22" in l and "%22Acme%22" in l for l in affine)


def test_out_file_and_overwrite_protection(tmp_path: Path) -> None:
    assert lancer("username", "jdupont", "--out", "liens.txt", cwd=tmp_path).returncode == 0
    contenu = (tmp_path / "liens.txt").read_text(encoding="utf-8")
    assert urls(contenu)
    refus = lancer("username", "jdupont", "--out", "liens.txt", cwd=tmp_path)
    assert refus.returncode == 2
    assert "existe déjà" in refus.stderr
    assert lancer("username", "jdupont", "--out", "liens.txt", "--force", cwd=tmp_path).returncode == 0


@pytest.mark.parametrize(
    ("args", "message"),
    [
        (["inconnu", "x"], "Mode inconnu"),
        (["mail"], "valeur principale manquante"),
        (["ville", "Lyon", "--ville", "Paris"], "affinage"),
    ],
)
def test_argument_errors(args: list[str], message: str) -> None:
    result = lancer(*args)
    assert result.returncode == 2
    assert message in result.stdout + result.stderr


def test_network_is_really_blocked() -> None:
    probe = (
        "import socket,sys\n"
        "def b(*a,**k): raise RuntimeError('x')\n"
        "socket.socket.connect=b\n"
        "try:\n socket.socket().connect(('127.0.0.1',9))\nexcept RuntimeError: sys.exit(0)\nsys.exit(1)\n"
    )
    assert subprocess.run([sys.executable, "-c", probe], check=False).returncode == 0
