"""Visual output: category cards (terminal) and a self-contained HTML report; URLs hidden behind labels."""

import shutil
import sys
from collections.abc import Mapping, Sequence
from html import escape
from io import StringIO

from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.style import Style
from rich.text import Text

from dorkint.output import to_google_url

_LABEL_MAX = 60


def dork_label(query: str) -> str:
    """Short single-line text shown instead of the long Google URL."""
    label = " ".join(query.split())
    return label if len(label) <= _LABEL_MAX else label[: _LABEL_MAX - 3] + "..."


def _unicode_printable() -> bool:
    """False when stdout's encoding cannot show box drawing (e.g. cp1252): ASCII fallback."""
    try:
        "╭▸".encode(sys.stdout.encoding or "ascii")
    except (UnicodeEncodeError, LookupError):
        return False
    return True


def render_cards(groups: Mapping[str, Sequence[str]], *, color: bool = False) -> str:
    """One panel per category; each label is a hyperlink (OSC 8) in terminals that support it."""
    if not groups:
        return ""
    width = min(shutil.get_terminal_size((80, 24)).columns, 100)
    buffer = StringIO()
    console = Console(file=buffer, width=width, force_terminal=color, color_system="standard" if color else None)
    unicode_ok = _unicode_printable()
    for category, dorks in groups.items():
        body = Group(*(Text(("▸ " if unicode_ok else "- ") + dork_label(d), style=Style(link=to_google_url(d))) for d in dorks))
        console.print(Panel(body, title=f"{category} ({len(dorks)})", title_align="left", box=box.ROUNDED if unicode_ok else box.ASCII))
    return buffer.getvalue().rstrip()


_CSS = """
:root{--bg:#f6f7fb;--card:#fff;--fg:#1c2230;--muted:#667;--accent:#3b6ef5;--line:#e3e6ef}
@media(prefers-color-scheme:dark){:root{--bg:#12151d;--card:#1b2030;--fg:#e8ebf5;--muted:#9aa3b8;--accent:#7aa2ff;--line:#2b3247}}
*{box-sizing:border-box}
body{margin:0;padding:24px 16px;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif}
main{max-width:1100px;margin:0 auto}
h1{margin:0 0 4px}
.sub{color:var(--muted);margin:0 0 16px}
button{background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:6px 12px;margin-right:8px;cursor:pointer}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;margin-top:16px;align-items:start}
details{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px}
summary{cursor:pointer;font-weight:600;list-style:none;display:flex;align-items:center;gap:8px}
summary::-webkit-details-marker{display:none}
.count{margin-left:auto;background:var(--accent);color:#fff;border-radius:999px;padding:0 10px;font-size:.85em}
.pills{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.pills a{color:var(--accent);border:1px solid var(--line);border-radius:999px;padding:3px 12px;font-size:.9em;text-decoration:none;word-break:break-word}
.pills a:hover,.pills a:focus-visible{background:var(--accent);color:#fff}
"""

_JS = """
const toggle = open => document.querySelectorAll('details').forEach(d => d.open = open);
document.getElementById('open').onclick = () => toggle(true);
document.getElementById('close').onclick = () => toggle(false);
"""


def render_html(groups: Mapping[str, Sequence[str]], *, title: str = "Dorkint") -> str:
    cards = []
    for category, dorks in groups.items():
        pills = "".join(
            f'<a href="{escape(to_google_url(d))}" target="_blank" rel="noopener noreferrer">'
            f"{escape(dork_label(d))}</a>"
            for d in dorks
        )
        cards.append(
            f'<details><summary>{escape(category)}'
            f'<span class="count">{len(dorks)}</span></summary><div class="pills">{pills}</div></details>'
        )
    total = sum(len(d) for d in groups.values())
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{escape(title)}</title><style>{_CSS}</style></head><body><main>"
        f'<h1>{escape(title)}</h1><p class="sub">{total} links in {len(groups)} categories. Click a card to open it.</p>'
        '<button id="open" type="button">Expand all</button><button id="close" type="button">Collapse all</button>'
        f'<div class="grid">{"".join(cards)}</div></main><script>{_JS}</script></body></html>'
    )
