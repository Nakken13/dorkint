"""Mode `fullname`: public information about a person (FR sources)."""

from dorkint.builder import Category, Mode, Template, register

register(Mode(
    name="fullname",
    refinements=("city", "company"),
    categories=(
        Category("Social networks", (
            Template("site:linkedin.com/in {primary}"),
            Template("site:linkedin.com/in {primary} {city}", requires=("city",)),
            Template("site:linkedin.com/in {primary} {company}", requires=("company",)),
            Template("site:facebook.com {primary}"),
            Template("site:facebook.com {primary} {city}", requires=("city",)),
            Template("site:instagram.com {primary}"),
            Template("(site:x.com OR site:twitter.com) {primary}"),
            Template("(site:x.com OR site:twitter.com) {primary} {city}", requires=("city",)),
            Template("site:github.com {primary}"),
            Template("site:github.com {primary} {company}", requires=("company",)),
        )),
        Category("Named CVs and PDFs", (
            Template("filetype:pdf {primary} cv"),
            Template("filetype:pdf {primary} curriculum vitae"),
            Template("filetype:pdf {primary} cv {city}", requires=("city",)),
            Template("filetype:pdf {primary} cv {company}", requires=("company",)),
            Template("filetype:pdf {primary} {city} {company}", requires=("city", "company")),
        )),
        Category("Academic work", (
            Template("site:theses.fr {primary}"),
            Template("site:hal.science {primary}"),
            Template("filetype:pdf {primary} mémoire"),
            Template("site:hal.science {primary} {company}", requires=("company",)),
            Template("filetype:pdf {primary} mémoire {city}", requires=("city",)),
        )),
        Category("Public appearances", (
            Template("{primary} conférence intervenant"),
            Template("site:meetup.com {primary}"),
            Template("site:youtube.com {primary}"),
            Template("{primary} conférence {city}", requires=("city",)),
            Template("site:youtube.com {primary} {company}", requires=("company",)),
        )),
        Category("Public records", (
            Template("site:journal-officiel.gouv.fr {primary}"),
            Template("site:bodacc.fr {primary}"),
            Template("site:data.gouv.fr {primary}"),
            Template("site:bodacc.fr {primary} {city}", requires=("city",)),
            Template("site:bodacc.fr {primary} {company}", requires=("company",)),
        )),
        Category("Portfolios", (
            Template("(site:behance.net OR site:dribbble.com) {primary}"),
            Template("{primary} portfolio"),
            Template("{primary} portfolio {city}", requires=("city",)),
            Template("{primary} portfolio {company}", requires=("company",)),
        )),
        Category("Press", (
            Template("{primary} interview OR article"),
            Template("site:lemonde.fr OR site:lefigaro.fr OR site:liberation.fr {primary}"),
            Template("{primary} {city} article", requires=("city",)),
            Template("{primary} {company} interview", requires=("company",)),
            Template("{primary} {city} {company}", requires=("city", "company")),
        )),
    ),
))
