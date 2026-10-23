import pytest

from dorkint import builder
from dorkint.builder import Category, Dork, DorkintError, Mode, Template, generate


@pytest.fixture
def fake_mode(monkeypatch: pytest.MonkeyPatch) -> Mode:
    mode = Mode(
        name="fake",
        refinements=("city", "company"),
        categories=(
            Category("Base", (Template('site:exemple.fr {primary}'),)),
            Category(
                "Crossed",
                (
                    Template("{primary} {city}", requires=("city",)),
                    Template("{primary} {city} {company}", requires=("city", "company")),
                ),
            ),
            Category("Brut", (Template("site:{primary:raw}"),)),
        ),
    )
    monkeypatch.setitem(builder._REGISTRY, "fake", mode)
    return mode


def test_placeholder_is_quoted(fake_mode: Mode) -> None:
    result = generate("fake", "Jean Dupont", {})
    assert result["Base"] == [Dork("Base", 'site:exemple.fr "Jean Dupont"')]


def test_raw_placeholder_is_not_quoted(fake_mode: Mode) -> None:
    assert generate("fake", "exemple.fr", {})["Brut"][0].query == "site:exemple.fr"


def test_quotes_in_value_are_removed(fake_mode: Mode) -> None:
    assert generate("fake", 'Jean "le" Dupont', {})["Base"][0].query == 'site:exemple.fr "Jean le Dupont"'


def test_absent_refinement_gives_only_base_dorks(fake_mode: Mode) -> None:
    assert "Crossed" not in generate("fake", "Jean", {})
    assert "Crossed" not in generate("fake", "Jean", {"city": None, "company": ""})


def test_present_refinement_adds_cross_variants(fake_mode: Mode) -> None:
    queries = [d.query for d in generate("fake", "Jean", {"city": "Lyon"})["Crossed"]]
    assert queries == ['"Jean" "Lyon"']
    both = [d.query for d in generate("fake", "Jean", {"city": "Lyon", "company": "Acme"})["Crossed"]]
    assert both == ['"Jean" "Lyon"', '"Jean" "Lyon" "Acme"']


def test_empty_principal_rejected(fake_mode: Mode) -> None:
    with pytest.raises(DorkintError, match="empty"):
        generate("fake", "   ", {})


def test_unknown_mode_rejected() -> None:
    with pytest.raises(DorkintError, match="Unknown mode"):
        generate("nexistepas", "x", {})


def test_unsupported_refinement_rejected(fake_mode: Mode) -> None:
    with pytest.raises(DorkintError, match="refinement"):
        generate("fake", "x", {"telephone": "1"})


def test_template_with_undeclared_placeholder_rejected() -> None:
    with pytest.raises(DorkintError, match="city"):
        Template("{primary} {city}")


def test_mode_without_categories_rejected() -> None:
    with pytest.raises(DorkintError, match="no category"):
        Mode("empty", (), ())


def test_duplicate_queries_are_dropped(monkeypatch: pytest.MonkeyPatch) -> None:
    mode = Mode("dup", (), (Category("A", (Template("{primary}"), Template("{primary}"))),))
    monkeypatch.setitem(builder._REGISTRY, "dup", mode)
    assert len(generate("dup", "x", {})["A"]) == 1


def test_register_rejects_duplicate_name(fake_mode: Mode) -> None:
    with pytest.raises(DorkintError, match="already registered"):
        builder.register(fake_mode)


def test_modes_discovered_from_package(tmp_path: object) -> None:
    # automatic loading must not fail on the modes package (even when empty)
    builder.load_modes()


def test_variantes_render_principal_as_or_group(monkeypatch: pytest.MonkeyPatch) -> None:
    mode = Mode(
        "multi",
        (),
        (Category("A", (Template("{primary} annuaire"),)),),
        variants=lambda v: [v, v.replace(" ", "")],
    )
    monkeypatch.setitem(builder._REGISTRY, "multi", mode)
    assert generate("multi", "06 12", {})["A"][0].query == '("06 12" OR "0612") annuaire'


def test_derive_adds_placeholders_usable_in_templates(monkeypatch: pytest.MonkeyPatch) -> None:
    mode = Mode(
        "derive",
        (),
        (Category("A", (Template("{primary} {local:raw} @{domain:raw}", requires=("local", "domain")),)),),
        derive=lambda v: dict(zip(("local", "domain"), v.split("@"), strict=True)),
        derived=("local", "domain"),
    )
    monkeypatch.setitem(builder._REGISTRY, "derive", mode)
    assert generate("derive", "jean@exemple.fr", {})["A"][0].query == '"jean@exemple.fr" jean @exemple.fr'


def test_derived_placeholder_must_be_declared() -> None:
    with pytest.raises(DorkintError, match="undeclared"):
        Mode("x", (), (Category("A", (Template("{primary} {local}", requires=("local",)),)),))


def test_derive_cannot_override_or_add_undeclared_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    mode = Mode(
        "derive2",
        (),
        (Category("A", (Template("{primary}"),)),),
        derive=lambda v: {"primary": "PIRATE", "unknown": "x", "local": ' a "b" '},
        derived=("local",),
    )
    monkeypatch.setitem(builder._REGISTRY, "derive2", mode)
    assert generate("derive2", "jean", {})["A"][0].query == '"jean"'


def test_variantes_are_deduplicated_and_raw_ignores_them(monkeypatch: pytest.MonkeyPatch) -> None:
    mode = Mode(
        "multi2",
        (),
        (Category("A", (Template("{primary}"), Template("inurl:{primary:raw}"))),),
        variants=lambda v: [v, v, f'"{v}"', v + "2"],
    )
    monkeypatch.setitem(builder._REGISTRY, "multi2", mode)
    requetes = [d.query for d in generate("multi2", "x", {})["A"]]
    assert requetes == ['("x" OR "x2")', "inurl:x"]


def test_keyword_is_appended_quoted_to_every_query(fake_mode: Mode) -> None:
    result = generate("fake", "Jean", {"city": "Lyon"}, keyword="minecraft")
    queries = [d.query for dorks in result.values() for d in dorks]
    assert queries and all(q.endswith(' "minecraft"') for q in queries)
    assert result["Base"][0].query == 'site:exemple.fr "Jean" "minecraft"'


def test_keyword_blank_or_none_changes_nothing(fake_mode: Mode) -> None:
    base = generate("fake", "Jean", {})
    assert generate("fake", "Jean", {}, keyword=None) == base
    assert generate("fake", "Jean", {}, keyword="  ") == base


def test_keyword_quotes_are_removed(fake_mode: Mode) -> None:
    assert generate("fake", "Jean", {}, keyword='mine"craft')["Base"][0].query.endswith(' "minecraft"')


def test_keyword_forbidden_term_is_rejected(fake_mode: Mode) -> None:
    with pytest.raises(DorkintError, match="password"):
        generate("fake", "Jean", {}, keyword="password")
