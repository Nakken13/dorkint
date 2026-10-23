"""Mode `phone`: French phone number."""

import re

from dorkint.builder import Category, Mode, Template, register

_FR = re.compile(r"^(?:0|\+?33|0033)(\d{9})$")


def phone_variants(number: str) -> list[str]:
    """Equivalent formats of a FR number; input unchanged if it is not a FR number.

    Plugged into the mode via `Mode.variants`: `{primary}` becomes `("a" OR "b" ...)`.
    """
    raw = re.sub(r"[\s.\-()]", "", number.replace("(0)", ""))
    match = _FR.match(raw)
    if not match:
        return [number]
    n = match.group(1)  # 9 digits without the leading 0
    pairs = [n[i:i + 2] for i in range(1, 9, 2)]
    return [
        f"0{n[0]} {' '.join(pairs)}",
        f"0{n[0]}.{'.'.join(pairs)}",
        f"0{n}",
        f"+33 {n[0]} {' '.join(pairs)}",
        f"+33{n}",
    ]


register(Mode(
    name="phone",
    refinements=("city", "company"),
    variants=phone_variants,
    categories=(
        Category("Reverse directories", (
            Template("site:pagesjaunes.fr {primary}"),
            Template("site:118712.fr {primary}"),
            Template("site:pagesjaunes.fr {primary} {city}", requires=("city",)),
            Template("site:118712.fr {primary} {city}", requires=("city",)),
        )),
        Category("Mentions web", (
            Template("{primary}"),
            Template("{primary} {city}", requires=("city",)),
            Template("{primary} {company}", requires=("company",)),
            Template("{primary} {city} {company}", requires=("city", "company")),
        )),
        Category("Social networks", (
            Template("site:facebook.com {primary}"),
            Template("site:linkedin.com {primary}"),
            Template("site:twitter.com OR site:instagram.com {primary}"),
            Template("site:linkedin.com {primary} {company}", requires=("company",)),
        )),
        Category("Classifieds", (
            Template("site:leboncoin.fr {primary}"),
            Template("site:vinted.fr {primary}"),
            Template("site:leboncoin.fr {primary} {city}", requires=("city",)),
        )),
        Category("Documents", (
            Template("filetype:pdf {primary}"),
            Template("filetype:doc OR filetype:docx {primary}"),
            Template("filetype:pdf {primary} {city}", requires=("city",)),
            Template("filetype:pdf {primary} {company}", requires=("company",)),
        )),
        Category("Company sites", (
            Template("intext:contact {primary}"),
            Template("inurl:contact {primary}"),
            Template("intext:contact {primary} {company}", requires=("company",)),
            Template("inurl:contact {primary} {city}", requires=("city",)),
        )),
    ),
))
