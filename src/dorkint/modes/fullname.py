"""Mode `fullname` : recherche d'informations publiques sur une personne (sources FR)."""

from dorkint.builder import Category, Mode, Template, register

register(Mode(
    name="fullname",
    refinements=("city", "company"),
    categories=(
        Category("Réseaux sociaux", (
            Template("site:linkedin.com/in {principal}"),
            Template("site:linkedin.com/in {principal} {city}", requires=("city",)),
            Template("site:linkedin.com/in {principal} {company}", requires=("company",)),
            Template("site:facebook.com {principal}"),
            Template("site:facebook.com {principal} {city}", requires=("city",)),
            Template("site:instagram.com {principal}"),
            Template("(site:x.com OR site:twitter.com) {principal}"),
            Template("(site:x.com OR site:twitter.com) {principal} {city}", requires=("city",)),
            Template("site:github.com {principal}"),
            Template("site:github.com {principal} {company}", requires=("company",)),
        )),
        Category("CV et PDF nominatifs", (
            Template("filetype:pdf {principal} cv"),
            Template("filetype:pdf {principal} curriculum vitae"),
            Template("filetype:pdf {principal} cv {city}", requires=("city",)),
            Template("filetype:pdf {principal} cv {company}", requires=("company",)),
            Template("filetype:pdf {principal} {city} {company}", requires=("city", "company")),
        )),
        Category("Travaux académiques", (
            Template("site:theses.fr {principal}"),
            Template("site:hal.science {principal}"),
            Template("filetype:pdf {principal} mémoire"),
            Template("site:hal.science {principal} {company}", requires=("company",)),
            Template("filetype:pdf {principal} mémoire {city}", requires=("city",)),
        )),
        Category("Interventions publiques", (
            Template("{principal} conférence intervenant"),
            Template("site:meetup.com {principal}"),
            Template("site:youtube.com {principal}"),
            Template("{principal} conférence {city}", requires=("city",)),
            Template("site:youtube.com {principal} {company}", requires=("company",)),
        )),
        Category("Actes publics", (
            Template("site:journal-officiel.gouv.fr {principal}"),
            Template("site:bodacc.fr {principal}"),
            Template("site:data.gouv.fr {principal}"),
            Template("site:bodacc.fr {principal} {city}", requires=("city",)),
            Template("site:bodacc.fr {principal} {company}", requires=("company",)),
        )),
        Category("Portfolios", (
            Template("(site:behance.net OR site:dribbble.com) {principal}"),
            Template("{principal} portfolio"),
            Template("{principal} portfolio {city}", requires=("city",)),
            Template("{principal} portfolio {company}", requires=("company",)),
        )),
        Category("Presse", (
            Template("{principal} interview OR article"),
            Template("site:lemonde.fr OR site:lefigaro.fr OR site:liberation.fr {principal}"),
            Template("{principal} {city} article", requires=("city",)),
            Template("{principal} {company} interview", requires=("company",)),
            Template("{principal} {city} {company}", requires=("city", "company")),
        )),
    ),
))
