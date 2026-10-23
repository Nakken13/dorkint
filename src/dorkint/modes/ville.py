"""Mode `ville` : recherche d'informations publiques sur une ville française."""

from dorkint.builder import Category, Mode, Template, register

register(Mode(
    name="ville",
    refinements=("entreprise",),
    categories=(
        Category("Institutions locales", (
            Template("{principal} mairie site:gouv.fr"),
            Template("{principal} site:data.gouv.fr"),
            Template("{principal} préfecture site:gouv.fr"),
            Template("{principal} mairie {entreprise}", requires=("entreprise",)),
        )),
        Category("Actualités locales", (
            Template("{principal} actualités presse régionale"),
            Template("{principal} site:ouest-france.fr OR site:ladepeche.fr OR site:leparisien.fr"),
            Template("{principal} {entreprise} actualités", requires=("entreprise",)),
        )),
        Category("Associations et événements", (
            Template("{principal} associations annuaire"),
            Template("{principal} agenda événements"),
            Template("{principal} {entreprise} événement", requires=("entreprise",)),
        )),
        Category("Entreprises locales", (
            Template("{principal} site:societe.com"),
            Template("{principal} site:infogreffe.fr"),
            Template("{principal} site:pagesjaunes.fr"),
            Template("{principal} {entreprise} site:societe.com", requires=("entreprise",)),
            Template("{principal} {entreprise} site:pagesjaunes.fr", requires=("entreprise",)),
        )),
        Category("Offres d'emploi locales", (
            Template("{principal} offres d'emploi"),
            Template("{principal} recrutement site:francetravail.fr"),
            Template("{principal} {entreprise} recrute", requires=("entreprise",)),
        )),
        Category("Documents publics", (
            Template("{principal} délibérations conseil municipal filetype:pdf"),
            Template("{principal} compte rendu conseil municipal filetype:pdf"),
            Template("{principal} {entreprise} filetype:pdf", requires=("entreprise",)),
        )),
        Category("Réseaux sociaux locaux", (
            Template("{principal} site:facebook.com/groups"),
            Template("{principal} site:facebook.com"),
            Template("{principal} {entreprise} site:facebook.com", requires=("entreprise",)),
        )),
    ),
))
