"""End-to-end tests: real `python -m dorkint` process, network forbidden."""

import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

SRC = Path(__file__).resolve().parents[2] / "src"
# Runs dorkint after making every network connection fail.
NO_NETWORK = (
    "import socket, runpy, sys\n"
    "def _blocked(*a, **k): raise RuntimeError('network access forbidden')\n"
    "socket.socket.connect = _blocked\n"
    "socket.create_connection = _blocked\n"
    "sys.argv[0] = 'dorkint'\n"
    "runpy.run_module('dorkint', run_name='__main__')\n"
)
VALUES = {
    "fullname": "Jean Dupont",
    "username": "jdupont",
    "site": "exemple.fr",
    "email": "jean.dupont@exemple.fr",
    "phone": "06 12 34 56 78",
    "company": "Acme",
}


def run_dorkint(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PYTHONPATH": str(SRC), "PYTHONIOENCODING": "utf-8"}
    return subprocess.run(
        [sys.executable, "-c", NO_NETWORK, *args],
        capture_output=True, text=True, encoding="utf-8", env=env, cwd=cwd, timeout=60, check=False,
    )


def urls(sortie: str) -> list[str]:
    return [line for line in sortie.splitlines() if line.startswith("http")]


@pytest.mark.parametrize(("mode", "value"), VALUES.items())
def test_mode_outputs_decodable_google_urls(mode: str, value: str) -> None:
    result = run_dorkint(mode, value)
    assert result.returncode == 0, result.stderr
    liens = urls(result.stdout)
    assert liens
    for lien in liens:
        parsed = urlparse(lien)
        assert (parsed.scheme, parsed.netloc, parsed.path) == ("https", "www.google.com", "/search")
        assert parse_qs(parsed.query)["q"][0].strip()
    requetes = [parse_qs(urlparse(l).query)["q"][0] for l in liens]
    cle = value if mode == "site" else f'"{value}"'
    assert any(cle in q for q in requetes)


def test_refinements_cross_variants() -> None:
    base = urls(run_dorkint("fullname", "Jean Dupont").stdout)
    affine = urls(run_dorkint("fullname", "Jean Dupont", "--city", "Lyon", "--company", "Acme").stdout)
    assert len(affine) > len(base)
    assert any("%22Lyon%22" in l and "%22Acme%22" in l for l in affine)


def test_out_file_and_overwrite_protection(tmp_path: Path) -> None:
    assert run_dorkint("username", "jdupont", "--out", "liens.txt", cwd=tmp_path).returncode == 0
    contenu = (tmp_path / "liens.txt").read_text(encoding="utf-8")
    assert urls(contenu)
    refusal = run_dorkint("username", "jdupont", "--out", "liens.txt", cwd=tmp_path)
    assert refusal.returncode == 2
    assert "already exists" in refusal.stderr
    assert run_dorkint("username", "jdupont", "--out", "liens.txt", "--force", cwd=tmp_path).returncode == 0


@pytest.mark.parametrize(
    ("args", "message"),
    [
        (["unknown", "x"], "Unknown mode"),
        (["email"], "missing primary value"),
        (["site", "exemple.fr", "--city", "Paris"], "refinement"),
    ],
)
def test_argument_errors(args: list[str], message: str) -> None:
    result = run_dorkint(*args)
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
