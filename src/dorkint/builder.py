"""Moteur pur de génération de dorks : modèle, registre des modes, `generer`."""

import importlib
import pkgutil
import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass

from dorkint.guardrails import termes_interdits

_PLACEHOLDER = re.compile(r"\{(\w+)(?::(raw))?\}")


class DorkintError(ValueError):
    """Erreur d'utilisation ou de déclaration, message destiné à l'utilisateur."""


@dataclass(frozen=True)
class Template:
    """Patron de requête ; `{principal}`, `{ville}`... sont insérés entre guillemets,
    `{principal:raw}` tel quel. `requires` : affinages nécessaires pour générer ce patron."""

    pattern: str
    requires: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        allowed = {"principal", *self.requires}
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
    """`variantes` : écritures alternatives du principal, rendues `("a" OR "b")`.
    `derive` : valeurs calculées depuis le principal, nommées dans `derived`."""

    name: str
    refinements: tuple[str, ...]
    categories: tuple[Category, ...]
    variantes: Callable[[str], list[str]] | None = None
    derive: Callable[[str], Mapping[str, str]] | None = None
    derived: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.categories:
            raise DorkintError(f"Le mode '{self.name}' n'a aucune catégorie.")
        for template in (t for c in self.categories for t in c.templates):
            unknown = set(template.requires) - set(self.refinements) - set(self.derived)
            if unknown:
                raise DorkintError(f"Mode '{self.name}' : affinage(s) non déclaré(s) {sorted(unknown)}.")


@dataclass(frozen=True)
class Dork:
    category: str
    query: str


_REGISTRY: dict[str, Mode] = {}


def register(mode: Mode) -> Mode:
    if mode.name in _REGISTRY:
        raise DorkintError(f"Le mode '{mode.name}' est déjà enregistré.")
    for category in mode.categories:
        for texte in (category.name, *(t.pattern for t in category.templates)):
            if interdits := termes_interdits(texte):
                raise DorkintError(
                    f"Mode '{mode.name}' : terme(s) interdit(s) {interdits} dans '{texte}' (garde-fou credentials)."
                )
    _REGISTRY[mode.name] = mode
    return mode


def load_modes() -> None:
    """Importe chaque module de `dorkint.modes` (qui s'enregistre à l'import)."""
    package = importlib.import_module("dorkint.modes")
    for info in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"dorkint.modes.{info.name}")


def get_mode(name: str) -> Mode:
    load_modes()
    if name not in _REGISTRY:
        raise DorkintError(f"Mode inconnu : '{name}'. Modes disponibles : {', '.join(_REGISTRY)}.")
    return _REGISTRY[name]


def _render(template: Template, values: Mapping[str, str], variantes: Sequence[str] = ()) -> str:
    def substitute(match: re.Match[str]) -> str:
        name, raw = match.groups()
        value = values[name]
        if raw:
            return value
        if name == "principal" and len(variantes) > 1:
            return "(" + " OR ".join(f'"{v}"' for v in variantes) + ")"
        return f'"{value}"'

    return _PLACEHOLDER.sub(substitute, template.pattern)


def _clean(value: str | None) -> str:
    return (value or "").replace('"', "").strip()


def generer(
    mode_name: str, principal: str, affinages: Mapping[str, str | None] | None = None
) -> dict[str, list[Dork]]:
    """Dorks du mode, groupés par catégorie (catégories vides omises)."""
    mode = get_mode(mode_name)
    principal = _clean(principal)
    if not principal:
        raise DorkintError("La valeur principale est vide.")
    unsupported = {k for k, v in (affinages or {}).items() if _clean(v)} - set(mode.refinements)
    if unsupported:
        raise DorkintError(f"Mode '{mode.name}' : affinage(s) non supporté(s) {sorted(unsupported)}.")
    values = {"principal": principal}
    values.update({k: c for k, v in (affinages or {}).items() if (c := _clean(v))})
    if mode.derive:
        values.update(mode.derive(principal))
    variantes = [c for v in mode.variantes(principal) if (c := _clean(v))] if mode.variantes else []

    result: dict[str, list[Dork]] = {}
    for category in mode.categories:
        seen: set[str] = set()
        for template in category.templates:
            if not all(r in values for r in template.requires):
                continue
            query = _render(template, values, variantes)
            if query not in seen:
                seen.add(query)
                result.setdefault(category.name, []).append(Dork(category.name, query))
    return result
