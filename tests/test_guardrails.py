import pytest

from dorkint.builder import DorkintError, generate, refinements_of
from dorkint.guardrails import FORBIDDEN_TERMS, forbidden_terms
from dorkint.modes import MODES


@pytest.mark.parametrize("terme", FORBIDDEN_TERMS)
def test_each_forbidden_term_is_detected(terme: str) -> None:
    assert forbidden_terms(f'site:exemple.fr "{terme}"') == [terme]
    assert forbidden_terms(f"intitle:{terme.upper()}") == [terme]


@pytest.mark.parametrize(
    "text", ['site:exemple.fr "Jean Dupont"', "town hall secretariat", "filetype:pdf cv", "tokenization"]
)
def test_healthy_text_passes(text: str) -> None:
    assert forbidden_terms(text) == []


def test_every_mode_is_clean_or_explicitly_site_scoped() -> None:
    """Forbidden terms are only tolerated on a `site`-mode pattern anchored to `site:{raw}`
    (see DISCLAIMER.md § No credentials)."""
    for name, mode in MODES.items():
        for category, patterns in mode.CATEGORIES.items():
            assert forbidden_terms(category) == [], (name, category)
            for pattern in patterns:
                if forbidden_terms(pattern):
                    assert name == "site" and pattern.startswith("site:{raw} "), (name, pattern)


def test_every_generated_query_is_clean_or_anchored_to_the_audited_site() -> None:
    for name in MODES:
        value = "exemple.fr" if name == "site" else "Jean Dupont"
        refinements = {r: "Lyon" for r in refinements_of(name)}
        for dorks in generate(name, value, refinements).values():
            for dork in dorks:
                if forbidden_terms(dork):
                    assert name == "site" and dork.startswith(f"site:{value} "), (name, dork)


def test_forbidden_keyword_is_rejected() -> None:
    with pytest.raises(DorkintError, match="password"):
        generate("fullname", "Jean", keyword="password")
