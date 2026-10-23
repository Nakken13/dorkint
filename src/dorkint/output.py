"""Output: dorks -> clickable Google URLs, grouped display, file saving."""

from collections.abc import Mapping, Sequence
from pathlib import Path
from urllib.parse import quote_plus

from dorkint.builder import Dork, DorkintError, Mode

_GOOGLE = "https://www.google.com/search?q="


def to_google_url(query: str) -> str:
    return _GOOGLE + quote_plus(query)


def format_dorks(groups: Mapping[str, Sequence[Dork]]) -> str:
    """One URL per line under a `## Category` header (nothing that breaks ctrl+click)."""
    blocks = [
        "\n".join([f"## {category}", *(to_google_url(d.query) for d in dorks)])
        for category, dorks in groups.items()
    ]
    return "\n\n".join(blocks)


def format_info(modes: Sequence[Mode]) -> str:
    """Raw patterns of each mode; `[...]` = required refinements (`--x`) or derived values."""
    blocks = []
    for mode in modes:
        lines = [f"# {mode.name}"]
        for category in mode.categories:
            lines.append(f"## {category.name}")
            for t in category.templates:
                required = ", ".join(f"--{r}" if r in mode.refinements else r for r in t.requires)
                lines.append(f"{t.pattern}  [{required}]" if required else t.pattern)
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def save(text: str, path: Path, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        raise DorkintError(f"File '{path}' already exists (use --force to overwrite it).")
    try:
        path.write_text(text, encoding="utf-8")
    except OSError as error:
        raise DorkintError(f"Cannot write '{path}': {error.strerror}.") from error
