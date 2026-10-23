"""Mode `site` : reconnaissance de surface sur un domaine que l'on est autorisé à auditer."""

from dorkint.builder import Category, Mode, Template, register

register(
    Mode(
        name="site",
        refinements=("company",),
        categories=(
            Category(
                "Sous-domaines",
                (
                    Template("site:*.{principal:raw} -www"),
                    Template("site:*.*.{principal:raw} -www"),
                ),
            ),
            Category(
                "Pages de connexion et d'administration visibles",
                (
                    Template("site:{principal:raw} inurl:login"),
                    Template("site:{principal:raw} inurl:admin"),
                    Template("site:{principal:raw} intitle:\"espace client\" OR intitle:\"espace membre\""),
                ),
            ),
            Category(
                "Documents exposés",
                (
                    Template("site:{principal:raw} filetype:pdf"),
                    Template("site:{principal:raw} filetype:doc OR filetype:docx"),
                    Template("site:{principal:raw} filetype:xls OR filetype:xlsx"),
                    Template("site:{principal:raw} filetype:ppt OR filetype:pptx"),
                    Template('site:{principal:raw} filetype:pdf "confidentiel"'),
                    Template('site:{principal:raw} filetype:pdf "usage interne"'),
                ),
            ),
            Category(
                "Listings de répertoires",
                (
                    Template('site:{principal:raw} intitle:"index of"'),
                    Template('site:{principal:raw} intitle:"index of" "parent directory"'),
                ),
            ),
            Category(
                "Pages d'erreur et technologies",
                (
                    Template('site:{principal:raw} "page not found" OR "page introuvable"'),
                    Template('site:{principal:raw} "powered by"'),
                    Template('site:{principal:raw} intitle:"erreur" OR intitle:"error"'),
                ),
            ),
            Category(
                "Mentions ailleurs",
                (
                    Template('-site:{principal:raw} "{principal:raw}"'),
                    Template('-site:{principal:raw} "{principal:raw}" avis OR critiques'),
                    Template('-site:{principal:raw} {principal} {company}', requires=("company",)),
                ),
            ),
            Category(
                "Offres d'emploi",
                (
                    Template('site:{principal:raw} inurl:careers OR inurl:carrieres OR inurl:recrutement'),
                    Template('site:{principal:raw} "offre d\'emploi" OR "nous recrutons"'),
                    Template(
                        'site:linkedin.com/jobs OR site:indeed.fr {company}',
                        requires=("company",),
                    ),
                ),
            ),
            Category(
                "Presse",
                (
                    Template('-site:{principal:raw} "{principal:raw}" presse OR communiqué'),
                    Template('"{principal:raw}" intitle:interview OR intitle:article'),
                    Template('{company} "{principal:raw}" actualités', requires=("company",)),
                ),
            ),
        ),
    )
)
