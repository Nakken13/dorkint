"""Mode `company`: company name or SIREN, French sources only."""

from dorkint.builder import Category, Mode, Template, register

register(
    Mode(
        name="company",
        refinements=("city",),
        categories=(
            Category(
                "FR registers",
                (
                    Template("site:infogreffe.fr {primary}"),
                    Template("site:societe.com {primary}"),
                    Template("site:pagesjaunes.fr {primary}"),
                    Template("site:pappers.fr {primary}"),
                    Template("site:annuaire-entreprises.data.gouv.fr {primary}"),
                    Template("site:societe.com {primary} {city}", requires=("city",)),
                    Template("site:pagesjaunes.fr {primary} {city}", requires=("city",)),
                ),
            ),
            Category(
                "data.gouv.fr and Journal Officiel / BODACC",
                (
                    Template("site:data.gouv.fr {primary}"),
                    Template("site:bodacc.fr {primary}"),
                    Template("site:journal-officiel.gouv.fr {primary}"),
                    Template("site:bodacc.fr {primary} {city}", requires=("city",)),
                ),
            ),
            Category(
                "Job offers",
                (
                    Template("site:welcometothejungle.com {primary}"),
                    Template("site:indeed.fr {primary}"),
                    Template("site:linkedin.com/jobs {primary}"),
                    Template("site:apec.fr {primary}"),
                    Template("site:indeed.fr {primary} {city}", requires=("city",)),
                ),
            ),
            Category(
                "Press and social networks",
                (
                    Template("site:linkedin.com/company {primary}"),
                    Template("site:facebook.com {primary}"),
                    Template("site:x.com {primary}"),
                    Template("{primary} actualité presse"),
                    Template("{primary} {city} actualité presse", requires=("city",)),
                ),
            ),
            Category(
                "Subdomains and exposed files",
                (
                    Template("{primary} filetype:pdf"),
                    Template("{primary} filetype:xlsx OR filetype:docx"),
                    Template("{primary} inurl:intranet OR inurl:extranet"),
                    Template("{primary} {city} filetype:pdf", requires=("city",)),
                ),
            ),
            Category(
                "Executives and officers",
                (
                    Template("{primary} dirigeant OR président OR gérant"),
                    Template("site:pappers.fr {primary} dirigeants"),
                    Template("site:linkedin.com/in {primary} fondateur OR directeur"),
                    Template("{primary} {city} dirigeant", requires=("city",)),
                ),
            ),
        ),
    )
)
