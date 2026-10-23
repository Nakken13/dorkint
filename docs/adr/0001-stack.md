# ADR 0001 — Choix de la stack

Statut : accepté (2026-10-23)

## Décision

Python (>= 3.11) pour dorkint.

## Contexte

dorkint génère des requêtes Google dorks (manipulation de chaînes, aucun
réseau) et affiche des liens cliquables dans le terminal. Projet solo, open
source, pièce de portfolio cyber. Candidats : C++, Python, Java.

## Raisons

1. Le problème est du texte : `urllib.parse.quote_plus` (stdlib) couvre
   l'encodage URL ; C++ n'a pas d'équivalent stdlib.
2. Aucune toolchain à installer (JDK + Gradle ou MSVC + CMake sinon).
3. L'écosystème OSINT/sécurité est surtout en Python (theHarvester, sherlock,
   Recon-ng) : le dépôt est lisible pour un recruteur cyber.
4. Distribution : `pipx install dorkint` / `uv tool install dorkint`.
5. Liens cliquables (OSC 8) gérés par `rich`.

## Alternatives rejetées

- **C++** : aucun gain de performance ici, toolchain et packaging lourds.
- **Java** : verbeux, JDK + Gradle imposés, pas d'écosystème OSINT.
- **Rust/Go** : pas de domination claire, courbe d'apprentissage pour un solo.

## Outils

| Rôle | Outil |
|------|-------|
| Packaging | `pyproject.toml` (PEP 621), backend `hatchling` |
| CLI | `typer` (embarque `rich`) |
| Tests | `pytest` (+ `typer.testing.CliRunner` pour le CLI) |
| Lint/format | `ruff` |
| Types | `mypy --strict` |
| CI | GitHub Actions (Windows + Linux) |

Version minimale : 3.11 (version installée sur la machine de dev ; 3.12+
recommandé par l'architecte mais non requis).

## Structure

```text
pyproject.toml
src/dorkint/        cli.py, builder.py, output.py, modes/<mode>.py
tests/              test_*.py, test_modes/
docs/adr/
```
