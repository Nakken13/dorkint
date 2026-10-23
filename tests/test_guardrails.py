import pytest

from dorkint import builder
from dorkint.builder import Category, DorkintError, Mode, Template, generate
from dorkint.guardrails import FORBIDDEN_TERMS, forbidden_terms


@pytest.mark.parametrize("terme", FORBIDDEN_TERMS)
def test_each_forbidden_term_is_detected(terme: str) -> None:
    assert forbidden_terms(f'site:exemple.fr "{terme}"') == [terme]
    assert forbidden_terms(f"intitle:{terme.upper()}") == [terme]


@pytest.mark.parametrize(
    "text", ['site:exemple.fr "Jean Dupont"', "town hall secretariat", "filetype:pdf cv", "tokenization"]
)
def test_healthy_text_passes(text: str) -> None:
    assert forbidden_terms(text) == []


def test_register_rejects_forbidden_template(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(builder, "_REGISTRY", {})
    bad = Mode("bad", (), (Category("X", (Template('filetype:env DB_PASSWORD {primary}'),)),))
    with pytest.raises(DorkintError, match="forbidden"):
        builder.register(bad)
    assert "bad" not in builder._REGISTRY


def test_register_rejects_credentials_exception_outside_site_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """The scoped exception is `site`-only: no other mode may opt in."""
    monkeypatch.setattr(builder, "_REGISTRY", {})
    bad = Mode(
        "bad",
        (),
        (Category("X", (Template('site:{primary:raw} filetype:env "password"', allow_credentials=True),)),),
    )
    with pytest.raises(DorkintError, match="forbidden"):
        builder.register(bad)


def test_register_rejects_credentials_exception_without_site_anchor(monkeypatch: pytest.MonkeyPatch) -> None:
    """`allow_credentials=True` only exempts a template that is itself anchored to `site:{primary:raw}`."""
    monkeypatch.setattr(builder, "_REGISTRY", {})
    bad = Mode(
        "site",
        (),
        (Category("X", (Template('"password" {primary}', allow_credentials=True),)),),
    )
    with pytest.raises(DorkintError, match="forbidden"):
        builder.register(bad)


def test_register_accepts_site_scoped_credentials_template(monkeypatch: pytest.MonkeyPatch) -> None:
    """A `site`-anchored template may opt into the credentials guardrail exception."""
    monkeypatch.setattr(builder, "_REGISTRY", {})
    good = Mode(
        "site",
        (),
        (Category("X", (Template('site:{primary:raw} filetype:env "password"', allow_credentials=True),)),),
    )
    builder.register(good)
    assert "site" in builder._REGISTRY


def test_register_rejects_forbidden_category_name(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(builder, "_REGISTRY", {})
    bad = Mode("bad", (), (Category("Mots de passe", (Template("{primary}"),)),))
    with pytest.raises(DorkintError, match="forbidden"):
        builder.register(bad)


def test_register_accepts_healthy_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(builder, "_REGISTRY", {})
    builder.register(Mode("sain", (), (Category("X", (Template("{primary}"),)),)))


def test_every_registered_mode_is_clean_or_explicitly_site_scoped() -> None:
    """Forbidden terms are only tolerated on a `site`-mode template anchored to `site:{primary:raw}`
    and explicitly opted in via `allow_credentials=True` (see DISCLAIMER.md § No credentials)."""
    builder.load_modes()
    assert builder._REGISTRY, "no mode loaded"
    for mode in builder._REGISTRY.values():
        for category in mode.categories:
            assert forbidden_terms(category.name) == [], (mode.name, category.name)
            for template in category.templates:
                if not forbidden_terms(template.pattern):
                    continue
                assert mode.name == "site" and template.allow_credentials, (mode.name, template.pattern)
                assert template.pattern.startswith("site:{primary:raw} "), (mode.name, template.pattern)


def test_every_generated_query_is_clean_or_anchored_to_the_audited_site() -> None:
    builder.load_modes()
    for name, mode in builder._REGISTRY.items():
        value = "exemple.fr" if name == "site" else "Jean Dupont"
        refinements = {r: "Lyon" for r in mode.refinements}
        for dorks in generate(name, value, refinements).values():
            for dork in dorks:
                if not forbidden_terms(dork.query):
                    continue
                assert name == "site" and dork.query.startswith(f"site:{value} "), (name, dork.query)
