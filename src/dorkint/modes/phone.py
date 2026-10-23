"""Mode `tel` : numéro de téléphone français."""

import re

from dorkint.builder import Category, Mode, Template, register

_FR = re.compile(r"^(?:0|\+?33|0033)(\d{9})$")


def variantes_tel(numero: str) -> list[str]:
    """Formats équivalents d'un numéro FR ; saisie inchangée si ce n'est pas un numéro FR.

    Branchée sur le mode via `Mode.variantes` : `{principal}` devient `("a" OR "b" ...)`.
    """
    brut = re.sub(r"[\s.\-()]", "", numero.replace("(0)", ""))
    match = _FR.match(brut)
    if not match:
        return [numero]
    n = match.group(1)  # 9 chiffres sans le 0 initial
    paires = [n[i:i + 2] for i in range(1, 9, 2)]
    return [
        f"0{n[0]} {' '.join(paires)}",
        f"0{n[0]}.{'.'.join(paires)}",
        f"0{n}",
        f"+33 {n[0]} {' '.join(paires)}",
        f"+33{n}",
    ]


register(Mode(
    name="phone",
    refinements=("city", "company"),
    variantes=variantes_tel,
    categories=(
        Category("Annuaires inversés", (
            Template("site:pagesjaunes.fr {principal}"),
            Template("site:118712.fr {principal}"),
            Template("site:pagesjaunes.fr {principal} {city}", requires=("city",)),
            Template("site:118712.fr {principal} {city}", requires=("city",)),
        )),
        Category("Mentions web", (
            Template("{principal}"),
            Template("{principal} {city}", requires=("city",)),
            Template("{principal} {company}", requires=("company",)),
            Template("{principal} {city} {company}", requires=("city", "company")),
        )),
        Category("Réseaux sociaux", (
            Template("site:facebook.com {principal}"),
            Template("site:linkedin.com {principal}"),
            Template("site:twitter.com OR site:instagram.com {principal}"),
            Template("site:linkedin.com {principal} {company}", requires=("company",)),
        )),
        Category("Annonces", (
            Template("site:leboncoin.fr {principal}"),
            Template("site:vinted.fr {principal}"),
            Template("site:leboncoin.fr {principal} {city}", requires=("city",)),
        )),
        Category("Documents", (
            Template("filetype:pdf {principal}"),
            Template("filetype:doc OR filetype:docx {principal}"),
            Template("filetype:pdf {principal} {city}", requires=("city",)),
            Template("filetype:pdf {principal} {company}", requires=("company",)),
        )),
        Category("Sites d'entreprise", (
            Template("intext:contact {principal}"),
            Template("inurl:contact {principal}"),
            Template("intext:contact {principal} {company}", requires=("company",)),
            Template("inurl:contact {principal} {city}", requires=("city",)),
        )),
    ),
))
