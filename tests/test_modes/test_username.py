import re

from dorkint.builder import generer, get_mode

FORBIDDEN = ("password", "passwd", "mot de passe", "secret", "token", "api_key", ".env", "credentials", "id_rsa", "dump")
EXPECTED_CATEGORIES = {
    "Profils réseaux sociaux",
    "Forums et communautés",
    "Code et dépôts",
    "Portfolios et blogs",
    "Mentions dans des PDF",
    "Mentions presse",
}


def test_mode_registered_with_refinements() -> None:
    mode = get_mode("username")
    assert set(mode.refinements) == {"ville", "entreprise"}
    assert EXPECTED_CATEGORIES <= {c.name for c in mode.categories}


def test_each_category_has_at_least_one_dork() -> None:
    result = generer("username", "jdupont42", {})
    assert EXPECTED_CATEGORIES <= set(result)
    assert all(result[name] for name in EXPECTED_CATEGORIES)


def test_main_value_injected_and_quoted() -> None:
    result = generer("username", "jdupont42", {})
    for dorks in result.values():
        for dork in dorks:
            assert '"jdupont42"' in dork.query


def test_social_platforms_covered() -> None:
    queries = " ".join(d.query for d in generer("username", "x1", {})["Profils réseaux sociaux"])
    for site in ("github.com", "x.com", "twitter.com", "instagram.com", "tiktok.com", "reddit.com", "youtube.com", "linkedin.com", "twitch.tv"):
        assert f"site:{site}" in queries


def test_pdf_and_french_sources() -> None:
    result = generer("username", "x1", {})
    assert all("filetype:pdf" in d.query for d in result["Mentions dans des PDF"])
    assert any("site:.fr" in d.query or ".fr" in d.query for d in result["Mentions presse"])


def test_refinements_cross() -> None:
    base = generer("username", "x1", {})
    crossed = generer("username", "x1", {"ville": "Lyon", "entreprise": "Acme"})
    count = lambda r: sum(len(v) for v in r.values())
    assert count(crossed) > count(base)
    queries = [d.query for v in crossed.values() for d in v]
    assert any('"Lyon"' in q for q in queries)
    assert any('"Acme"' in q for q in queries)
    assert any('"Lyon"' in q and '"Acme"' in q for q in queries)
    assert not any('"Lyon"' in d.query for v in base.values() for d in v)


def test_no_credentials_terms() -> None:
    mode = get_mode("username")
    for category in mode.categories:
        for template in category.templates:
            lowered = template.pattern.lower()
            for term in FORBIDDEN:
                assert not re.search(re.escape(term), lowered), (term, template.pattern)
