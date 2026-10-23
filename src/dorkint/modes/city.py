"""Mode `city`: public information about a French city."""

from dorkint.builder import Category, Mode, Template, register

register(Mode(
    name="city",
    refinements=("company",),
    categories=(
        Category("Local institutions", (
            Template("{primary} mairie site:gouv.fr"),
            Template("{primary} site:data.gouv.fr"),
            Template("{primary} préfecture site:gouv.fr"),
            Template("{primary} mairie {company}", requires=("company",)),
        )),
        Category("Local news", (
            Template("{primary} actualités presse régionale"),
            Template("{primary} site:ouest-france.fr OR site:ladepeche.fr OR site:leparisien.fr"),
            Template("{primary} {company} actualités", requires=("company",)),
        )),
        Category("Associations and events", (
            Template("{primary} associations annuaire"),
            Template("{primary} agenda événements"),
            Template("{primary} {company} événement", requires=("company",)),
        )),
        Category("Local businesses", (
            Template("{primary} site:societe.com"),
            Template("{primary} site:infogreffe.fr"),
            Template("{primary} site:pagesjaunes.fr"),
            Template("{primary} {company} site:societe.com", requires=("company",)),
            Template("{primary} {company} site:pagesjaunes.fr", requires=("company",)),
        )),
        Category("Local job offers", (
            Template("{primary} offres d'emploi"),
            Template("{primary} recrutement site:francetravail.fr"),
            Template("{primary} {company} recrute", requires=("company",)),
        )),
        Category("Public documents", (
            Template("{primary} délibérations conseil municipal filetype:pdf"),
            Template("{primary} compte rendu conseil municipal filetype:pdf"),
            Template("{primary} {company} filetype:pdf", requires=("company",)),
        )),
        Category("Local social networks", (
            Template("{primary} site:facebook.com/groups"),
            Template("{primary} site:facebook.com"),
            Template("{primary} {company} site:facebook.com", requires=("company",)),
        )),
    ),
))
