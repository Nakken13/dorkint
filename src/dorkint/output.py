"""Output: dorks -> clickable Google URLs, grouped display, file saving."""

from collections.abc import Mapping, Sequence
from pathlib import Path
from urllib.parse import quote_plus

from dorkint.builder import DorkintError, needs, refinements_of
from dorkint.modes import MODES

_GOOGLE = "https://www.google.com/search?q="


def to_google_url(query: str) -> str:
    return _GOOGLE + quote_plus(query)


def format_dorks(groups: Mapping[str, Sequence[str]]) -> str:
    """One URL per line under a `## Category` header (nothing that breaks ctrl+click)."""
    blocks = [
        "\n".join([f"## {category}", *(to_google_url(d) for d in dorks)])
        for category, dorks in groups.items()
    ]
    return "\n\n".join(blocks)


def format_info() -> str:
    """Raw patterns of each mode; `[...]` = required refinements (`--x`) or derived values."""
    blocks = []
    for name, mode in MODES.items():
        lines = [f"# {name}"]
        for category, patterns in mode.CATEGORIES.items():
            lines.append(f"## {category}")
            for pattern in patterns:
                required = ", ".join(f"--{n}" if n in refinements_of(name) else n for n in needs(pattern))
                lines.append(f"{pattern}  [{required}]" if required else pattern)
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def save(text: str, path: Path, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        raise DorkintError(f"File '{path}' already exists (use --force to overwrite it).")
    try:
        path.write_text(text, encoding="utf-8")
    except OSError as error:
        raise DorkintError(f"Cannot write '{path}': {error.strerror}.") from error
