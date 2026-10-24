"""Visual output: category cards (terminal) and a self-contained HTML report; URLs hidden behind labels."""

import shutil
import sys
from collections.abc import Mapping, Sequence
from html import escape
from io import StringIO

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.rule import Rule
from rich.style import Style
from rich.table import Table
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


def render_menu(
    title: str,
    options: Sequence[str],
    *,
    columns: int = 1,
    back: str = "Back",
    info: bool = False,
    color: bool = False,
) -> str:
    """Numbered menu in a panel: key badge + option name laid out row by row over `columns` columns;
    the info and back keys sit below a rule."""
    terminal = shutil.get_terminal_size((80, 24)).columns
    buffer = StringIO()
    console = Console(file=buffer, width=terminal, force_terminal=color, color_system="256" if color else None)
    unicode_ok = _unicode_printable()
    rows = Table.grid(padding=(0, 2), expand=True)
    for _ in range(columns):
        rows.add_column(justify="right")
        rows.add_column(no_wrap=True, ratio=1)
    cells = [
        (Text(f"[{number}]", style="bold cyan"), Text(option, style="bold"))
        for number, option in enumerate(options, start=1)
    ]
    for start in range(0, len(cells), columns):
        line = cells[start : start + columns]
        missing = columns - len(line)
        line = [(Text(""), Text(""))] * (missing // 2) + line + [(Text(""), Text(""))] * (missing - missing // 2)
        rows.add_row(*(cell for pair in line for cell in pair))
    rule = Rule(style="dim", characters="─" if unicode_ok else "-")
    keys = Text()
    if info:
        keys.append("[0]", style="bold cyan").append("  Info", style="dim").append("        ")
    keys.append("[q]", style="bold color(208)").append(f"  {back}", style="dim")
    back_row = Align.center(keys)
    panel = Panel(
        Group(rows, rule, back_row),
        title=Text(title, style="bold"),
        title_align="left",
        box=box.ROUNDED if unicode_ok else box.ASCII,
        border_style="cyan",
        padding=(0, 2),
        width=min(terminal, 64),
    )
    console.print(Align.center(panel))
    return "\n".join(line.rstrip() for line in buffer.getvalue().splitlines())


def render_info(title: str, lines: Sequence[str], *, color: bool = False) -> str:
    """Centered panel (same width as the menu) with one wrapped paragraph per line."""
    terminal = shutil.get_terminal_size((80, 24)).columns
    buffer = StringIO()
    console = Console(file=buffer, width=terminal, force_terminal=color, color_system="256" if color else None)
    panel = Panel(
        Group(*(Text(line) for line in lines)),
        title=Text(title, style="bold"),
        title_align="left",
        box=box.ROUNDED if _unicode_printable() else box.ASCII,
        border_style="cyan",
        padding=(0, 2),
        width=min(terminal, 64),
    )
    console.print(Align.center(panel))
    return "\n".join(line.rstrip() for line in buffer.getvalue().splitlines())


def menu_prompt(*, color: bool = False) -> str:
    """Input prompt for the menus: `dorkint ❯ ` (bold white when `color`), ASCII `dorkint > ` if needed."""
    arrow = "❯" if _unicode_printable() else ">"
    text = f"dorkint {arrow}"
    return f"\x1b[1;97m{text}\x1b[0m " if color else f"{text} "


_CSS = """
:root{color-scheme:light dark;--bg:#f5f7f7;--card:#fff;--hover:#f0f4f4;--fg:#14191a;--muted:#51605f;--line:#d5dedd;--accent:#0b6b66;--on-accent:#fff;--focus:#c25a00}
@media(prefers-color-scheme:dark){:root{--bg:#0e1112;--card:#161b1d;--hover:#1c2326;--fg:#e6ecec;--muted:#9aabab;--line:#2a3436;--accent:#4fd1c5;--on-accent:#06201e;--focus:#ff9f43}}
*{box-sizing:border-box}
body{margin:0;padding:24px 16px;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:1200px;margin:0 auto}
h1{margin:0;font:700 28px/1.2 ui-monospace,SFMono-Regular,Consolas,monospace;overflow-wrap:anywhere}
h1 span{color:var(--focus)}
.sub{color:var(--muted);font-size:14px;margin:4px 0 0}
.bar{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px;padding:12px 0;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10;background:var(--bg)}
#q{display:none;flex:1 1 100%;min-height:44px;padding:0 12px;font-size:16px;background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:8px}
.js #q{display:block}
.bar button{flex:1;min-height:44px;background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:0 12px;font:inherit;font-size:14px;cursor:pointer}
.bar button:hover,#q:hover{border-color:var(--accent)}
:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:16px;margin-top:16px;align-items:start}
details{background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}
summary{cursor:pointer;font-size:15px;font-weight:600;list-style:none;display:flex;align-items:center;gap:8px;min-height:44px;padding:8px 16px}
summary::-webkit-details-marker{display:none}
summary:hover{background:var(--hover)}
summary::after{content:"";width:8px;height:8px;border:solid var(--muted);border-width:0 2px 2px 0;transform:rotate(-45deg);margin-left:4px}
details[open]>summary::after{transform:rotate(45deg)}
.count{margin-left:auto;border:1px solid var(--line);color:var(--muted);border-radius:999px;padding:0 10px;font-size:12px;font-weight:400;font-variant-numeric:tabular-nums}
.pills{display:flex;flex-wrap:wrap;gap:8px;padding:4px 16px 16px}
.pills a,.pills a:visited{display:inline-flex;align-items:center;min-height:32px;color:var(--accent);border:1px solid var(--line);border-radius:999px;padding:6px 12px;font:13px/1.3 ui-monospace,SFMono-Regular,Consolas,monospace;text-decoration:none;word-break:break-word}
.pills a::after{content:"\\2197";margin-left:6px;opacity:.6}
.pills a:hover{background:var(--accent);color:var(--on-accent);border-color:var(--accent)}
.pills a:active{transform:translateY(1px)}
.empty{text-align:center;color:var(--muted);padding:48px 16px}
.empty button{background:none;border:0;color:var(--accent);font:inherit;text-decoration:underline;cursor:pointer}
[hidden]{display:none!important}
@media(min-width:640px){body{padding:32px 24px}.bar button{flex:none}#q{flex:1 1 240px}}
@media(pointer:coarse){.pills a{min-height:44px}}
@media(prefers-reduced-motion:no-preference){summary,.pills a,.bar button{transition:background-color .12s ease-out,color .12s ease-out,border-color .12s ease-out}summary::after{transition:transform .12s ease-out}}
@media print{.bar{display:none}}
"""

_JS = r"""
document.documentElement.classList.add('js');
const $ = id => document.getElementById(id);
const norm = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
const items = [...document.querySelectorAll('details')].map(card => ({
  card, name: norm(card.dataset.name), badge: card.querySelector('.count'),
  pills: [...card.querySelectorAll('.pills a')].map(a => ({a, text: norm(a.textContent)})),
}));
const total = items.reduce((n, i) => n + i.pills.length, 0);
const stat = $('stat'), q = $('q'), empty = $('empty'), base = stat.textContent;
let saved = null, timer = 0;
const toggle = open => items.forEach(i => { if (!i.card.hidden) i.card.open = open; });
$('open').onclick = () => toggle(true);
$('close').onclick = () => toggle(false);
function apply() {
  const term = norm(q.value.trim());
  if (!term) {
    if (saved) items.forEach((i, k) => { i.card.open = saved[k]; });
    saved = null;
    items.forEach(i => { i.card.hidden = false; i.badge.textContent = i.pills.length; i.pills.forEach(p => { p.a.hidden = false; }); });
    stat.textContent = base; empty.hidden = !!total; $('msg').textContent = 'Nothing to show.'; $('clear').hidden = true;
    return;
  }
  if (!saved) saved = items.map(i => i.card.open);
  let links = 0, cats = 0;
  items.forEach(i => {
    const all = i.name.includes(term);
    let n = 0;
    i.pills.forEach(p => { p.a.hidden = !(all || p.text.includes(term)); if (!p.a.hidden) n++; });
    i.card.hidden = n === 0;
    i.badge.textContent = n + '/' + i.pills.length;
    if (n) { i.card.open = true; links += n; cats++; }
  });
  stat.textContent = links + ' of ' + total + ' links in ' + cats + ' of ' + items.length + ' categories';
  empty.hidden = links > 0;
  $('msg').textContent = 'No link matches "' + q.value.trim() + '".';
  $('clear').hidden = false;
}
q.oninput = () => { clearTimeout(timer); timer = setTimeout(apply, 80); };
const reset = () => { q.value = ''; apply(); };
$('clear').onclick = () => { reset(); q.focus(); };
document.addEventListener('keydown', e => {
  const typing = /^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName);
  if (e.key === '/' && !typing && !e.ctrlKey && !e.metaKey && !e.altKey) { e.preventDefault(); q.focus(); }
  else if (e.key === 'Escape' && document.activeElement === q) { reset(); q.blur(); }
});
window.addEventListener('beforeprint', () => items.forEach(i => { i.card.open = true; }));
"""

_OPEN_LIMIT = 12  # more categories than this start collapsed (the filter opens them on demand)


def render_html(groups: Mapping[str, Sequence[str]], *, title: str = "Dorkint") -> str:
    open_attr = " open" if len(groups) <= _OPEN_LIMIT else ""
    cards = []
    for category, dorks in groups.items():
        pills = "".join(
            f'<a href="{escape(to_google_url(d))}" target="_blank" rel="noopener noreferrer">'
            f"{escape(dork_label(d))}</a>"
            for d in dorks
        )
        cards.append(
            f'<details{open_attr} data-name="{escape(category)}"><summary>{escape(category)}'
            f'<span class="count">{len(dorks)}</span></summary><div class="pills">{pills}</div></details>'
        )
    total = sum(len(d) for d in groups.values())
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{escape(title)}</title><style>{_CSS}</style></head><body><main>"
        f'<h1><span aria-hidden="true">&#10095;</span> {escape(title)}</h1>'
        f'<p class="sub" id="stat" aria-live="polite">{total} links in {len(groups)} categories</p>'
        '<div class="bar"><input type="search" id="q" aria-label="Filter links" '
        'placeholder="Filter links… ( / )" autocomplete="off">'
        '<button id="open" type="button">Expand all</button><button id="close" type="button">Collapse all</button></div>'
        f'<div class="grid">{"".join(cards)}</div>'
        f'<div class="empty" id="empty" role="status"{"" if not groups else " hidden"}>'
        '<p id="msg">Nothing to show.</p><button id="clear" type="button" hidden>Clear filter</button></div>'
        f"</main><script>{_JS}</script></body></html>"
    )
