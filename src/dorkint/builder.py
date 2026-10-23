"""Pure dork-generation engine: model, mode registry, `generate`."""

import importlib
import pkgutil
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass

from dorkint.guardrails import forbidden_terms

_PLACEHOLDER = re.compile(r"\{(\w+)(?::(raw))?\}")


class DorkintError(ValueError):
    """Usage or declaration error; the message is meant for the user."""


@dataclass(frozen=True)
class Template:
    """Query pattern; `{primary}`, `{city}`... are inserted between quotes,
    `{primary:raw}` as is. `requires`: refinements needed to generate this pattern.
    `allow_credentials`: opts into the credentials-guardrail exception (see `register`);
    only ever usable on a `site`-mode template anchored to `site:{primary:raw}`
    (DISCLAIMER.md § No credentials)."""

    pattern: str
    requires: tuple[str, ...] = ()
    allow_credentials: bool = False

    def __post_init__(self) -> None:
        allowed = {"primary", *self.requires}
        for name, _ in _PLACEHOLDER.findall(self.pattern):
            if name not in allowed:
                raise DorkintError(
                    f"Template '{self.pattern}' : placeholder '{name}' absent de requires {self.requires}."
                )


@dataclass(frozen=True)
class Category:
    name: str
    templates: tuple[Template, ...]


@dataclass(frozen=True)
class Mode:
    """`variants`: alternative spellings of the primary value, rendered `("a" OR "b")`.
    `derive`: values computed from the primary value, named in `derived`."""

    name: str
    refinements: tuple[str, ...]
    categories: tuple[Category, ...]
    variants: Callable[[str], list[str]] | None = None
    derive: Callable[[str], Mapping[str, str]] | None = None
    derived: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.categories:
            raise DorkintError(f"Mode '{self.name}' has no category.")
        for template in (t for c in self.categories for t in c.templates):
            unknown = set(template.requires) - set(self.refinements) - set(self.derived)
            if unknown:
                raise DorkintError(f"Mode '{self.name}': undeclared refinement(s) {sorted(unknown)}.")


@dataclass(frozen=True)
class Dork:
    category: str
    query: str


_REGISTRY: dict[str, Mode] = {}


_SITE_SCOPE_ANCHOR = "site:{primary:raw} "


def _is_site_scoped_exception(mode_name: str, template: Template) -> bool:
    """The only tolerated carve-out from the credentials guardrail: a `site`-mode template
    that opts in explicitly and is itself anchored to the audited domain, never a generic
    web-wide search (DISCLAIMER.md § No credentials)."""
    return (
        mode_name == "site" and template.allow_credentials and template.pattern.startswith(_SITE_SCOPE_ANCHOR)
    )


def register(mode: Mode) -> Mode:
    if mode.name in _REGISTRY:
        raise DorkintError(f"Mode '{mode.name}' is already registered.")
    for category in mode.categories:
        if forbidden := forbidden_terms(category.name):
            raise DorkintError(
                f"Mode '{mode.name}': forbidden term(s) {forbidden} in '{category.name}' (credentials guardrail)."
            )
        for template in category.templates:
            if (forbidden := forbidden_terms(template.pattern)) and not _is_site_scoped_exception(
                mode.name, template
            ):
                raise DorkintError(
                    f"Mode '{mode.name}': forbidden term(s) {forbidden} in '{template.pattern}' "
                    "(credentials guardrail)."
                )
    _REGISTRY[mode.name] = mode
    return mode


def load_modes() -> None:
    """Imports every module of `dorkint.modes` (each registers itself on import)."""
    package = importlib.import_module("dorkint.modes")
    for info in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"dorkint.modes.{info.name}")


def get_mode(name: str) -> Mode:
    load_modes()
    if name not in _REGISTRY:
        raise DorkintError(f"Unknown mode: '{name}'. Available modes: {', '.join(_REGISTRY)}.")
    return _REGISTRY[name]


def _render(template: Template, values: Mapping[str, str], group: str | None = None) -> str:
    def substitute(match: re.Match[str]) -> str:
        name, raw = match.groups()
        if raw:
            return values[name]  # `:raw` also ignores the variants of the primary value
        return group if name == "primary" and group else f'"{values[name]}"'

    return _PLACEHOLDER.sub(substitute, template.pattern)


def _clean(value: str | None) -> str:
    return (value or "").replace('"', "").strip()


def generate(
    mode_name: str,
    primary: str,
    refinements: Mapping[str, str | None] | None = None,
    keyword: str | None = None,
) -> dict[str, list[Dork]]:
    """Dorks of the mode, grouped by category (empty categories omitted)."""
    mode = get_mode(mode_name)
    primary = _clean(primary)
    if not primary:
        raise DorkintError("The primary value is empty.")
    unsupported = {k for k, v in (refinements or {}).items() if _clean(v)} - set(mode.refinements)
    if unsupported:
        raise DorkintError(f"Mode '{mode.name}': unsupported refinement(s) {sorted(unsupported)}.")
    keyword = _clean(keyword)
    if forbidden := forbidden_terms(keyword):
        raise DorkintError(f"Keyword: forbidden term(s) {forbidden} (credentials guardrail).")
    suffix = f' "{keyword}"' if keyword else ""
    values = {"primary": primary}
    values.update({k: c for k, v in (refinements or {}).items() if (c := _clean(v))})
    if mode.derive:
        values.update({k: c for k, v in mode.derive(primary).items() if k in mode.derived and (c := _clean(v))})
    variants = list(dict.fromkeys(c for v in mode.variants(primary) if (c := _clean(v)))) if mode.variants else []
    group = "(" + " OR ".join(f'"{v}"' for v in variants) + ")" if len(variants) > 1 else None

    result: dict[str, list[Dork]] = {}
    for category in mode.categories:
        seen: set[str] = set()
        for template in category.templates:
            if not all(r in values for r in template.requires):
                continue
            query = _render(template, values, group) + suffix
            if query not in seen:
                seen.add(query)
                result.setdefault(category.name, []).append(Dork(category.name, query))
    return result
