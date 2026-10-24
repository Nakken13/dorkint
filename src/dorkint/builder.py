"""Dork generation: fills each mode's query patterns with the user's input."""

import re

from dorkint.guardrails import forbidden_terms
from dorkint.modes import MODES

REFINEMENTS = ("city", "company")


class DorkintError(ValueError):
    """Usage error; the message is meant for the user."""


def _clean(value):
    return (value or "").replace('"', "").strip()


def needs(pattern):
    """Refinements / derived values a pattern needs, in order of appearance."""
    return list(dict.fromkeys(n for n in re.findall(r"\{(\w+)\}", pattern) if n not in ("primary", "raw")))


def refinements_of(mode):
    """Refinements (`city`, `company`) that at least one pattern of the mode uses."""
    used = {n for patterns in MODES[mode].CATEGORIES.values() for p in patterns for n in needs(p)}
    return tuple(r for r in REFINEMENTS if r in used)


def generate(mode, primary, refinements=None, keyword=None):
    """Dorks of the mode as {category: [query]} (empty categories omitted)."""
    if mode not in MODES:
        raise DorkintError(f"Unknown mode: '{mode}'. Available modes: {', '.join(MODES)}.")
    primary = _clean(primary)
    if not primary:
        raise DorkintError("The primary value is empty.")
    given = {k: c for k, v in (refinements or {}).items() if (c := _clean(v))}
    if unsupported := set(given) - set(refinements_of(mode)):
        raise DorkintError(f"Mode '{mode}': unsupported refinement(s) {sorted(unsupported)}.")
    keyword = _clean(keyword)
    if forbidden := forbidden_terms(keyword):
        raise DorkintError(f"Keyword: forbidden term(s) {forbidden} (credentials guardrail).")
    suffix = f' "{keyword}"' if keyword else ""

    # {primary}, {city}... go between quotes; {raw} is the primary value as is
    values = {"primary": f'"{primary}"', "raw": primary} | {k: f'"{v}"' for k, v in given.items()}
    if hasattr(MODES[mode], "values"):
        values |= MODES[mode].values(primary)

    result = {}
    for category, patterns in MODES[mode].CATEGORIES.items():
        queries = [p.format_map(values) + suffix for p in patterns if all(values.get(n) for n in needs(p))]
        if queries := list(dict.fromkeys(queries)):
            result[category] = queries
    return result
