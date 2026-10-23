"""Mode `email`: public mentions of an email address (no leak database)."""

import re

from dorkint.builder import Category, Mode, Template, register

_ADDRESS = re.compile(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", re.IGNORECASE)


def _split(address: str) -> dict[str, str]:
    """Local part and domain of an address; empty if it is not an address."""
    if not _ADDRESS.fullmatch(address):
        return {}
    local, _, domain = address.partition("@")
    return {"local": local, "domain": domain}


register(
    Mode(
        name="email",
        refinements=("city", "company"),
        derive=_split,
        derived=("local", "domain"),
        categories=(
            Category(
                "Mentions web",
                (
                    Template("{primary}"),
                    Template("intext:{primary}"),
                    Template("{primary} contact"),
                    Template("{primary} {city}", requires=("city",)),
                    Template("{primary} {company}", requires=("company",)),
                    Template("{primary} {company} {city}", requires=("company", "city")),
                ),
            ),
            Category(
                "PDFs and documents",
                (
                    Template("filetype:pdf {primary}"),
                    Template("filetype:doc OR filetype:docx {primary}"),
                    Template("filetype:xls OR filetype:xlsx OR filetype:ppt {primary}"),
                    Template("filetype:pdf {primary} {company}", requires=("company",)),
                    Template("filetype:pdf {primary} {city}", requires=("city",)),
                ),
            ),
            Category(
                "Social networks and profiles",
                (
                    Template("site:linkedin.com {primary}"),
                    Template("site:facebook.com OR site:x.com OR site:instagram.com {primary}"),
                    Template("site:github.com OR site:gitlab.com {primary}"),
                    Template("site:linkedin.com {primary} {company}", requires=("company",)),
                    Template("site:linkedin.com OR site:facebook.com {primary} {city}", requires=("city",)),
                ),
            ),
            Category(
                "Forums and comments",
                (
                    Template("inurl:forum {primary}"),
                    Template("site:reddit.com OR site:stackoverflow.com {primary}"),
                    Template("intext:{primary} inurl:comment"),
                    Template("inurl:forum {primary} {city}", requires=("city",)),
                ),
            ),
            Category(
                "Directories and signatures",
                (
                    Template("site:societe.com OR site:pagesjaunes.fr {primary}"),
                    Template("intitle:annuaire {primary}"),
                    Template("{primary} cordialement"),
                    Template("{primary} tél mobile signature"),
                    Template("site:pagesjaunes.fr {primary} {city}", requires=("city",)),
                    Template("intitle:annuaire {primary} {company}", requires=("company",)),
                ),
            ),
            Category(
                "Press and publications",
                (
                    Template("{primary} communiqué de presse"),
                    Template("{primary} auteur publication"),
                    Template("site:hal.science OR site:researchgate.net {primary}"),
                    Template("{primary} communiqué {company}", requires=("company",)),
                ),
            ),
            Category(
                "Local part and domain",
                (
                    Template("{local} site:{domain:raw}", requires=("local", "domain")),
                    Template("{local} -site:{domain:raw}", requires=("local", "domain")),
                    Template("inurl:{primary}"),
                    Template("intitle:{primary}"),
                    Template("{primary} -site:linkedin.com -site:facebook.com"),
                    Template("{primary} -site:linkedin.com {company}", requires=("company",)),
                ),
            ),
        ),
    )
)
