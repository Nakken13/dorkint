"""Mode `entreprise` : raison sociale ou SIREN, sources françaises uniquement."""

from dorkint.builder import Category, Mode, Template, register

register(
    Mode(
        name="company",
        refinements=("city",),
        categories=(
            Category(
                "Registres FR",
                (
                    Template("site:infogreffe.fr {principal}"),
                    Template("site:societe.com {principal}"),
                    Template("site:pagesjaunes.fr {principal}"),
                    Template("site:pappers.fr {principal}"),
                    Template("site:annuaire-entreprises.data.gouv.fr {principal}"),
                    Template("site:societe.com {principal} {city}", requires=("city",)),
                    Template("site:pagesjaunes.fr {principal} {city}", requires=("city",)),
                ),
            ),
            Category(
                "data.gouv.fr et Journal Officiel / BODACC",
                (
                    Template("site:data.gouv.fr {principal}"),
                    Template("site:bodacc.fr {principal}"),
                    Template("site:journal-officiel.gouv.fr {principal}"),
                    Template("site:bodacc.fr {principal} {city}", requires=("city",)),
                ),
            ),
            Category(
                "Offres d'emploi",
                (
                    Template("site:welcometothejungle.com {principal}"),
                    Template("site:indeed.fr {principal}"),
                    Template("site:linkedin.com/jobs {principal}"),
                    Template("site:apec.fr {principal}"),
                    Template("site:indeed.fr {principal} {city}", requires=("city",)),
                ),
            ),
            Category(
                "Presse et réseaux sociaux",
                (
                    Template("site:linkedin.com/company {principal}"),
                    Template("site:facebook.com {principal}"),
                    Template("site:x.com {principal}"),
                    Template("{principal} actualité presse"),
                    Template("{principal} {city} actualité presse", requires=("city",)),
                ),
            ),
            Category(
                "Sous-domaines et fichiers exposés",
                (
                    Template("{principal} filetype:pdf"),
                    Template("{principal} filetype:xlsx OR filetype:docx"),
                    Template("{principal} inurl:intranet OR inurl:extranet"),
                    Template("{principal} {city} filetype:pdf", requires=("city",)),
                ),
            ),
            Category(
                "Dirigeants et mandataires",
                (
                    Template("{principal} dirigeant OR président OR gérant"),
                    Template("site:pappers.fr {principal} dirigeants"),
                    Template("site:linkedin.com/in {principal} fondateur OR directeur"),
                    Template("{principal} {city} dirigeant", requires=("city",)),
                ),
            ),
        ),
    )
)
