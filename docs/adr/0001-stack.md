# ADR 0001 — Stack choice

Status: accepted (2026-10-23)

## Decision

Python (>= 3.11) for dorkint.

## Context

dorkint generates Google dork queries (string manipulation, no network) and
prints clickable links in the terminal. Solo, open-source project, cyber
portfolio piece. Candidates: C++, Python, Java.

## Reasons

1. The problem is text: `urllib.parse.quote_plus` (stdlib) covers URL
   encoding; C++ has no stdlib equivalent.
2. No toolchain to install (otherwise JDK + Gradle or MSVC + CMake).
3. The OSINT/security ecosystem is mostly Python (theHarvester, sherlock,
   Recon-ng): the repository is readable for a cyber recruiter.
4. Distribution: `pipx install dorkint` / `uv tool install dorkint`.
5. Clickable links (OSC 8) handled by `rich`.

## Rejected alternatives

- **C++**: no performance gain here, heavy toolchain and packaging.
- **Java**: verbose, JDK + Gradle required, no OSINT ecosystem.
- **Rust/Go**: no clear advantage, learning curve for a solo developer.

## Tools

| Role | Tool |
|------|------|
| Packaging | `pyproject.toml` (PEP 621), `hatchling` backend |
| CLI | `typer` (bundles `rich`) |
| Tests | `pytest` (+ `typer.testing.CliRunner` for the CLI) |
| Lint/format | `ruff` |
| Types | `mypy --strict` |
| CI | GitHub Actions (Windows + Linux) |

Minimum version: 3.11 (version installed on the dev machine; 3.12+ recommended
by the architect but not required).

## Structure

```text
pyproject.toml
src/dorkint/        cli.py, builder.py, output.py, modes/<mode>.py
tests/              test_*.py, test_modes/
docs/adr/
```
