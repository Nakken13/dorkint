"""Mode `mail` : mentions publiques d'une adresse email (aucune base de fuite)."""

import re

from dorkint.builder import Category, Mode, Template, register

_ADRESSE = re.compile(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", re.IGNORECASE)


def _decouper(adresse: str) -> dict[str, str]:
    """Partie locale et domaine d'une adresse ; vide si ce n'est pas une adresse."""
    if not _ADRESSE.fullmatch(adresse):
        return {}
    local, _, domaine = adresse.partition("@")
    return {"local": local, "domaine": domaine}


register(
    Mode(
        name="email",
        refinements=("city", "company"),
        derive=_decouper,
        derived=("local", "domaine"),
        categories=(
            Category(
                "Mentions web",
                (
                    Template("{principal}"),
                    Template("intext:{principal}"),
                    Template("{principal} contact"),
                    Template("{principal} {city}", requires=("city",)),
                    Template("{principal} {company}", requires=("company",)),
                    Template("{principal} {company} {city}", requires=("company", "city")),
                ),
            ),
            Category(
                "PDF et documents",
                (
                    Template("filetype:pdf {principal}"),
                    Template("filetype:doc OR filetype:docx {principal}"),
                    Template("filetype:xls OR filetype:xlsx OR filetype:ppt {principal}"),
                    Template("filetype:pdf {principal} {company}", requires=("company",)),
                    Template("filetype:pdf {principal} {city}", requires=("city",)),
                ),
            ),
            Category(
                "Réseaux sociaux et profils",
                (
                    Template("site:linkedin.com {principal}"),
                    Template("site:facebook.com OR site:x.com OR site:instagram.com {principal}"),
                    Template("site:github.com OR site:gitlab.com {principal}"),
                    Template("site:linkedin.com {principal} {company}", requires=("company",)),
                    Template("site:linkedin.com OR site:facebook.com {principal} {city}", requires=("city",)),
                ),
            ),
            Category(
                "Forums et commentaires",
                (
                    Template("inurl:forum {principal}"),
                    Template("site:reddit.com OR site:stackoverflow.com {principal}"),
                    Template("intext:{principal} inurl:comment"),
                    Template("inurl:forum {principal} {city}", requires=("city",)),
                ),
            ),
            Category(
                "Annuaires et signatures",
                (
                    Template("site:societe.com OR site:pagesjaunes.fr {principal}"),
                    Template("intitle:annuaire {principal}"),
                    Template("{principal} cordialement"),
                    Template("{principal} tél mobile signature"),
                    Template("site:pagesjaunes.fr {principal} {city}", requires=("city",)),
                    Template("intitle:annuaire {principal} {company}", requires=("company",)),
                ),
            ),
            Category(
                "Presse et publications",
                (
                    Template("{principal} communiqué de presse"),
                    Template("{principal} auteur publication"),
                    Template("site:hal.science OR site:researchgate.net {principal}"),
                    Template("{principal} communiqué {company}", requires=("company",)),
                ),
            ),
            Category(
                "Partie locale et domaine",
                (
                    Template("{local} site:{domaine:raw}", requires=("local", "domaine")),
                    Template("{local} -site:{domaine:raw}", requires=("local", "domaine")),
                    Template("inurl:{principal}"),
                    Template("intitle:{principal}"),
                    Template("{principal} -site:linkedin.com -site:facebook.com"),
                    Template("{principal} -site:linkedin.com {company}", requires=("company",)),
                ),
            ),
        ),
    )
)
