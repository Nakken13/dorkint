"""Mode `tel` : numéro de téléphone français."""

import re

from dorkint.builder import Category, Mode, Template, register

_FR = re.compile(r"^(?:0|\+?33|0033)(\d{9})$")


def variantes_tel(numero: str) -> list[str]:
    """Formats équivalents d'un numéro FR ; saisie inchangée si ce n'est pas un numéro FR.

    Non utilisée par `generer` (un Template ne substitue qu'un `{principal}`), exportée pour
    une future gestion de variantes multiples par le moteur.
    """
    brut = re.sub(r"[\s.\-()]", "", numero)
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
    name="tel",
    refinements=("ville", "entreprise"),
    categories=(
        Category("Annuaires inversés", (
            Template("site:pagesjaunes.fr {principal}"),
            Template("site:118712.fr {principal}"),
            Template("site:pagesjaunes.fr {principal} {ville}", requires=("ville",)),
            Template("site:118712.fr {principal} {ville}", requires=("ville",)),
        )),
        Category("Mentions web", (
            Template("{principal}"),
            Template("{principal} {ville}", requires=("ville",)),
            Template("{principal} {entreprise}", requires=("entreprise",)),
            Template("{principal} {ville} {entreprise}", requires=("ville", "entreprise")),
        )),
        Category("Réseaux sociaux", (
            Template("site:facebook.com {principal}"),
            Template("site:linkedin.com {principal}"),
            Template("site:twitter.com OR site:instagram.com {principal}"),
            Template("site:linkedin.com {principal} {entreprise}", requires=("entreprise",)),
        )),
        Category("Annonces", (
            Template("site:leboncoin.fr {principal}"),
            Template("site:vinted.fr {principal}"),
            Template("site:leboncoin.fr {principal} {ville}", requires=("ville",)),
        )),
        Category("Documents", (
            Template("filetype:pdf {principal}"),
            Template("filetype:doc OR filetype:docx {principal}"),
            Template("filetype:pdf {principal} {ville}", requires=("ville",)),
            Template("filetype:pdf {principal} {entreprise}", requires=("entreprise",)),
        )),
        Category("Sites d'entreprise", (
            Template("intext:contact {principal}"),
            Template("inurl:contact {principal}"),
            Template("intext:contact {principal} {entreprise}", requires=("entreprise",)),
            Template("inurl:contact {principal} {ville}", requires=("ville",)),
        )),
    ),
))
