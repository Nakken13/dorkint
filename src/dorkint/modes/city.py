"""Mode `city`: public information about a French city."""

CATEGORIES = {
    'Local institutions': [
        '{primary} mairie site:gouv.fr',
        '{primary} site:data.gouv.fr',
        '{primary} préfecture site:gouv.fr',
        '{primary} mairie {company}',
    ],
    'Local news': [
        '{primary} actualités presse régionale',
        '{primary} site:ouest-france.fr OR site:ladepeche.fr OR site:leparisien.fr',
        '{primary} {company} actualités',
    ],
    'Associations and events': [
        '{primary} associations annuaire',
        '{primary} agenda événements',
        '{primary} {company} événement',
    ],
    'Local businesses': [
        '{primary} site:societe.com',
        '{primary} site:infogreffe.fr',
        '{primary} site:pagesjaunes.fr',
        '{primary} {company} site:societe.com',
        '{primary} {company} site:pagesjaunes.fr',
    ],
    'Local job offers': [
        "{primary} offres d'emploi",
        '{primary} recrutement site:francetravail.fr',
        '{primary} {company} recrute',
    ],
    'Public documents': [
        '{primary} délibérations conseil municipal filetype:pdf',
        '{primary} compte rendu conseil municipal filetype:pdf',
        '{primary} {company} filetype:pdf',
    ],
    'Local social networks': [
        '{primary} site:facebook.com/groups',
        '{primary} site:facebook.com',
        '{primary} {company} site:facebook.com',
    ],
}
