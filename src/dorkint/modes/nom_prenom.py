"""Mode `nom-prenom` : recherche d'informations publiques sur une personne (sources FR)."""

from dorkint.builder import Category, Mode, Template, register

register(Mode(
    name="nom-prenom",
    refinements=("ville", "entreprise"),
    categories=(
        Category("Réseaux sociaux", (
            Template("site:linkedin.com/in {principal}"),
            Template("site:linkedin.com/in {principal} {ville}", requires=("ville",)),
            Template("site:linkedin.com/in {principal} {entreprise}", requires=("entreprise",)),
            Template("site:facebook.com {principal}"),
            Template("site:facebook.com {principal} {ville}", requires=("ville",)),
            Template("site:instagram.com {principal}"),
            Template("(site:x.com OR site:twitter.com) {principal}"),
            Template("(site:x.com OR site:twitter.com) {principal} {ville}", requires=("ville",)),
            Template("site:github.com {principal}"),
            Template("site:github.com {principal} {entreprise}", requires=("entreprise",)),
        )),
        Category("CV et PDF nominatifs", (
            Template("filetype:pdf {principal} cv"),
            Template("filetype:pdf {principal} curriculum vitae"),
            Template("filetype:pdf {principal} cv {ville}", requires=("ville",)),
            Template("filetype:pdf {principal} cv {entreprise}", requires=("entreprise",)),
            Template("filetype:pdf {principal} {ville} {entreprise}", requires=("ville", "entreprise")),
        )),
        Category("Travaux académiques", (
            Template("site:theses.fr {principal}"),
            Template("site:hal.science {principal}"),
            Template("filetype:pdf {principal} mémoire"),
            Template("site:hal.science {principal} {entreprise}", requires=("entreprise",)),
            Template("filetype:pdf {principal} mémoire {ville}", requires=("ville",)),
        )),
        Category("Interventions publiques", (
            Template("{principal} conférence intervenant"),
            Template("site:meetup.com {principal}"),
            Template("site:youtube.com {principal}"),
            Template("{principal} conférence {ville}", requires=("ville",)),
            Template("site:youtube.com {principal} {entreprise}", requires=("entreprise",)),
        )),
        Category("Actes publics", (
            Template("site:journal-officiel.gouv.fr {principal}"),
            Template("site:bodacc.fr {principal}"),
            Template("site:data.gouv.fr {principal}"),
            Template("site:bodacc.fr {principal} {ville}", requires=("ville",)),
            Template("site:bodacc.fr {principal} {entreprise}", requires=("entreprise",)),
        )),
        Category("Portfolios", (
            Template("(site:behance.net OR site:dribbble.com) {principal}"),
            Template("{principal} portfolio"),
            Template("{principal} portfolio {ville}", requires=("ville",)),
            Template("{principal} portfolio {entreprise}", requires=("entreprise",)),
        )),
        Category("Presse", (
            Template("{principal} interview OR article"),
            Template("site:lemonde.fr OR site:lefigaro.fr OR site:liberation.fr {principal}"),
            Template("{principal} {ville} article", requires=("ville",)),
            Template("{principal} {entreprise} interview", requires=("entreprise",)),
            Template("{principal} {ville} {entreprise}", requires=("ville", "entreprise")),
        )),
    ),
))
