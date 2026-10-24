import re

from dorkint.builder import Dork
from dorkint.output import to_google_url
from dorkint.visual import category_icon, dork_label, render_cards, render_html

GROUPS = {
    "Social networks": [Dork("Social networks", 'site:x.com "a&b"'), Dork("Social networks", "site:y.com a")],
    "Documents": [Dork("Documents", "filetype:pdf a")],
}


def test_icon_matches_category_keyword_with_fallback() -> None:
    assert category_icon("Social networks") != category_icon("Documents")
    assert category_icon("Totally unknown") == "🔎"


def test_label_is_short_single_line() -> None:
    label = dork_label("x" * 200)
    assert len(label) <= 60 and label.endswith("...")
    assert dork_label("site:x.com a") == "site:x.com a"


def test_html_has_one_collapsible_card_per_category() -> None:
    html = render_html(GROUPS, title="Dorkint")
    assert html.count("<details") == len(GROUPS)
    assert "Social networks" in html and "Documents" in html
    assert ">2<" in html  # link count badge


def test_html_links_are_google_urls_and_hidden_behind_labels() -> None:
    html = render_html(GROUPS, title="Dorkint")
    hrefs = re.findall(r'href="([^"]+)"', html)
    assert len(hrefs) == 3
    assert all(h.startswith("https://www.google.com/search?q=") for h in hrefs)
    assert to_google_url("filetype:pdf a") in hrefs
    assert 'rel="noopener noreferrer"' in html
    assert ">filetype:pdf a</a>" in html  # visible text is the label, not the URL


def test_html_escapes_untrusted_text() -> None:
    evil = {"<script>alert(1)</script>": [Dork("c", '"><img src=x onerror=alert(1)>')]}
    html = render_html(evil, title="<b>t</b>")
    assert "<script>alert(1)" not in html
    assert "<img src=x" not in html
    assert "<b>t</b>" not in html


def test_html_empty_groups_still_valid_page() -> None:
    html = render_html({}, title="Dorkint")
    assert html.startswith("<!doctype html>") and "</html>" in html


def test_cards_show_category_count_and_labels_without_raw_urls() -> None:
    text = render_cards(GROUPS)
    assert "Social networks" in text and "Documents" in text
    assert "site:y.com a" in text
    assert "google.com" not in text


def test_cards_empty() -> None:
    assert render_cards({}) == ""


def test_cards_fall_back_to_ascii_when_stdout_cannot_encode(monkeypatch) -> None:
    import io
    import sys

    monkeypatch.setattr(sys, "stdout", io.TextIOWrapper(io.BytesIO(), encoding="cp1252"))
    text = render_cards(GROUPS)
    text.encode("cp1252")  # must not raise
    assert "Social networks (2)" in text
