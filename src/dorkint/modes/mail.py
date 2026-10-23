"""Mode `mail` : mentions publiques d'une adresse email (aucune base de fuite)."""

from dorkint.builder import Category, Mode, Template, register

register(
    Mode(
        name="mail",
        refinements=("ville", "entreprise"),
        categories=(
            Category(
                "Mentions web",
                (
                    Template("{principal}"),
                    Template("intext:{principal}"),
                    Template("{principal} contact"),
                    Template("{principal} {ville}", requires=("ville",)),
                    Template("{principal} {entreprise}", requires=("entreprise",)),
                    Template("{principal} {entreprise} {ville}", requires=("entreprise", "ville")),
                ),
            ),
            Category(
                "PDF et documents",
                (
                    Template("filetype:pdf {principal}"),
                    Template("filetype:doc OR filetype:docx {principal}"),
                    Template("filetype:xls OR filetype:xlsx OR filetype:ppt {principal}"),
                    Template("filetype:pdf {principal} {entreprise}", requires=("entreprise",)),
                    Template("filetype:pdf {principal} {ville}", requires=("ville",)),
                ),
            ),
            Category(
                "Réseaux sociaux et profils",
                (
                    Template("site:linkedin.com {principal}"),
                    Template("site:facebook.com OR site:x.com OR site:instagram.com {principal}"),
                    Template("site:github.com OR site:gitlab.com {principal}"),
                    Template("site:linkedin.com {principal} {entreprise}", requires=("entreprise",)),
                    Template("site:linkedin.com OR site:facebook.com {principal} {ville}", requires=("ville",)),
                ),
            ),
            Category(
                "Forums et commentaires",
                (
                    Template("inurl:forum {principal}"),
                    Template("site:reddit.com OR site:stackoverflow.com {principal}"),
                    Template("intext:{principal} inurl:comment"),
                    Template("inurl:forum {principal} {ville}", requires=("ville",)),
                ),
            ),
            Category(
                "Annuaires et signatures",
                (
                    Template("site:societe.com OR site:pagesjaunes.fr {principal}"),
                    Template("intitle:annuaire {principal}"),
                    Template("{principal} cordialement"),
                    Template("{principal} tél mobile signature"),
                    Template("site:pagesjaunes.fr {principal} {ville}", requires=("ville",)),
                    Template("intitle:annuaire {principal} {entreprise}", requires=("entreprise",)),
                ),
            ),
            Category(
                "Presse et publications",
                (
                    Template("{principal} communiqué de presse"),
                    Template("{principal} auteur publication"),
                    Template("site:hal.science OR site:researchgate.net {principal}"),
                    Template("{principal} communiqué {entreprise}", requires=("entreprise",)),
                ),
            ),
            Category(
                "Partie locale et domaine",
                (
                    Template("inurl:{principal}"),
                    Template("intitle:{principal}"),
                    Template("{principal} -site:linkedin.com -site:facebook.com"),
                    Template("{principal} -site:linkedin.com {entreprise}", requires=("entreprise",)),
                ),
            ),
        ),
    )
)
