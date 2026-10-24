from types import SimpleNamespace

import pytest

from dorkint import builder
from dorkint.builder import DorkintError, generate, refinements_of


@pytest.fixture
def fake_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = SimpleNamespace(
        CATEGORIES={
            "Base": ["site:exemple.fr {primary}"],
            "Crossed": ["{primary} {city}", "{primary} {city} {company}"],
            "Brut": ["site:{raw}"],
        }
    )
    monkeypatch.setitem(builder.MODES, "fake", fake)


def test_placeholder_is_quoted(fake_mode: None) -> None:
    assert generate("fake", "Jean Dupont")["Base"] == ['site:exemple.fr "Jean Dupont"']


def test_raw_placeholder_is_not_quoted(fake_mode: None) -> None:
    assert generate("fake", "exemple.fr")["Brut"] == ["site:exemple.fr"]


def test_quotes_in_value_are_removed(fake_mode: None) -> None:
    assert generate("fake", 'Jean "le" Dupont')["Base"] == ['site:exemple.fr "Jean le Dupont"']


def test_absent_refinement_gives_only_base_dorks(fake_mode: None) -> None:
    assert "Crossed" not in generate("fake", "Jean")
    assert "Crossed" not in generate("fake", "Jean", {"city": None, "company": ""})


def test_present_refinement_adds_cross_variants(fake_mode: None) -> None:
    assert generate("fake", "Jean", {"city": "Lyon"})["Crossed"] == ['"Jean" "Lyon"']
    both = generate("fake", "Jean", {"city": "Lyon", "company": "Acme"})["Crossed"]
    assert both == ['"Jean" "Lyon"', '"Jean" "Lyon" "Acme"']


def test_refinements_are_deduced_from_the_patterns(fake_mode: None) -> None:
    assert refinements_of("fake") == ("city", "company")


def test_empty_principal_rejected(fake_mode: None) -> None:
    with pytest.raises(DorkintError, match="empty"):
        generate("fake", "   ")


def test_unknown_mode_rejected() -> None:
    with pytest.raises(DorkintError, match="Unknown mode"):
        generate("nexistepas", "x")


def test_unsupported_refinement_rejected(fake_mode: None) -> None:
    with pytest.raises(DorkintError, match="refinement"):
        generate("fake", "x", {"telephone": "1"})


def test_duplicate_queries_are_dropped(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(builder.MODES, "dup", SimpleNamespace(CATEGORIES={"A": ["{primary}", "{primary}"]}))
    assert generate("dup", "x")["A"] == ['"x"']


def test_values_hook_adds_and_overrides_placeholders(monkeypatch: pytest.MonkeyPatch) -> None:
    mode = SimpleNamespace(
        CATEGORIES={"A": ["{primary} {local} @{domain}", "{primary} {other}"]},
        values=lambda v: dict(zip(("local", "domain"), v.split("@"), strict=True)) | {"primary": "P"},
    )
    monkeypatch.setitem(builder.MODES, "derive", mode)
    assert generate("derive", "jean@exemple.fr")["A"] == ["P jean @exemple.fr"]  # {other} is never given


def test_keyword_is_appended_quoted_to_every_query(fake_mode: None) -> None:
    result = generate("fake", "Jean", {"city": "Lyon"}, keyword="minecraft")
    queries = [q for qs in result.values() for q in qs]
    assert queries and all(q.endswith(' "minecraft"') for q in queries)
    assert result["Base"][0] == 'site:exemple.fr "Jean" "minecraft"'


def test_keyword_blank_or_none_changes_nothing(fake_mode: None) -> None:
    base = generate("fake", "Jean")
    assert generate("fake", "Jean", keyword=None) == base
    assert generate("fake", "Jean", keyword="  ") == base


def test_keyword_quotes_are_removed(fake_mode: None) -> None:
    assert generate("fake", "Jean", keyword='mine"craft')["Base"][0].endswith(' "minecraft"')


def test_keyword_forbidden_term_is_rejected(fake_mode: None) -> None:
    with pytest.raises(DorkintError, match="password"):
        generate("fake", "Jean", keyword="password")
