"""Mode `ville` : recherche d'informations publiques sur une ville française."""

from dorkint.builder import Category, Mode, Template, register

register(Mode(
    name="city",
    refinements=("company",),
    categories=(
        Category("Institutions locales", (
            Template("{principal} mairie site:gouv.fr"),
            Template("{principal} site:data.gouv.fr"),
            Template("{principal} préfecture site:gouv.fr"),
            Template("{principal} mairie {company}", requires=("company",)),
        )),
        Category("Actualités locales", (
            Template("{principal} actualités presse régionale"),
            Template("{principal} site:ouest-france.fr OR site:ladepeche.fr OR site:leparisien.fr"),
            Template("{principal} {company} actualités", requires=("company",)),
        )),
        Category("Associations et événements", (
            Template("{principal} associations annuaire"),
            Template("{principal} agenda événements"),
            Template("{principal} {company} événement", requires=("company",)),
        )),
        Category("Entreprises locales", (
            Template("{principal} site:societe.com"),
            Template("{principal} site:infogreffe.fr"),
            Template("{principal} site:pagesjaunes.fr"),
            Template("{principal} {company} site:societe.com", requires=("company",)),
            Template("{principal} {company} site:pagesjaunes.fr", requires=("company",)),
        )),
        Category("Offres d'emploi locales", (
            Template("{principal} offres d'emploi"),
            Template("{principal} recrutement site:francetravail.fr"),
            Template("{principal} {company} recrute", requires=("company",)),
        )),
        Category("Documents publics", (
            Template("{principal} délibérations conseil municipal filetype:pdf"),
            Template("{principal} compte rendu conseil municipal filetype:pdf"),
            Template("{principal} {company} filetype:pdf", requires=("company",)),
        )),
        Category("Réseaux sociaux locaux", (
            Template("{principal} site:facebook.com/groups"),
            Template("{principal} site:facebook.com"),
            Template("{principal} {company} site:facebook.com", requires=("company",)),
        )),
    ),
))
