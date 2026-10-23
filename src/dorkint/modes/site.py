"""Mode `site`: surface reconnaissance of a domain you are authorized to audit."""

from dorkint.builder import Category, Mode, Template, register

register(
    Mode(
        name="site",
        refinements=("company",),
        categories=(
            Category(
                "Subdomains",
                (
                    Template("site:*.{primary:raw} -www"),
                    Template("site:*.*.{primary:raw} -www"),
                ),
            ),
            Category(
                "Visible login and admin pages",
                (
                    Template("site:{primary:raw} inurl:login"),
                    Template("site:{primary:raw} inurl:admin"),
                    Template("site:{primary:raw} intitle:\"espace client\" OR intitle:\"espace membre\""),
                ),
            ),
            Category(
                "Exposed documents",
                (
                    Template("site:{primary:raw} filetype:pdf"),
                    Template("site:{primary:raw} filetype:doc OR filetype:docx"),
                    Template("site:{primary:raw} filetype:xls OR filetype:xlsx"),
                    Template("site:{primary:raw} filetype:ppt OR filetype:pptx"),
                    Template('site:{primary:raw} filetype:pdf "confidentiel"'),
                    Template('site:{primary:raw} filetype:pdf "usage interne"'),
                ),
            ),
            Category(
                "Directory listings",
                (
                    Template('site:{primary:raw} intitle:"index of"'),
                    Template('site:{primary:raw} intitle:"index of" "parent directory"'),
                ),
            ),
            Category(
                "Sensitive files exposed on the site",
                (
                    Template('site:{primary:raw} intitle:"index of" (filetype:sql OR filetype:log OR filetype:bak)'),
                    Template('site:{primary:raw} (ext:git OR ext:svn) intitle:"index of"'),
                    Template(
                        'site:{primary:raw} filetype:env "DB_PASSWORD"',
                        allow_credentials=True,
                    ),
                    Template(
                        'site:{primary:raw} inurl:"wp-config" (filetype:txt OR filetype:bak)',
                        allow_credentials=True,
                    ),
                    Template(
                        'site:{primary:raw} filetype:log inurl:"password"',
                        allow_credentials=True,
                    ),
                ),
            ),
            Category(
                "Error pages and technologies",
                (
                    Template('site:{primary:raw} "page not found" OR "page introuvable"'),
                    Template('site:{primary:raw} "powered by"'),
                    Template('site:{primary:raw} intitle:"error" OR intitle:"error"'),
                ),
            ),
            Category(
                "Mentions elsewhere",
                (
                    Template('-site:{primary:raw} "{primary:raw}"'),
                    Template('-site:{primary:raw} "{primary:raw}" avis OR critiques'),
                    Template('-site:{primary:raw} {primary} {company}', requires=("company",)),
                ),
            ),
            Category(
                "Job offers",
                (
                    Template('site:{primary:raw} inurl:careers OR inurl:carrieres OR inurl:recrutement'),
                    Template('site:{primary:raw} "offre d\'emploi" OR "nous recrutons"'),
                    Template(
                        'site:linkedin.com/jobs OR site:indeed.fr {company}',
                        requires=("company",),
                    ),
                ),
            ),
            Category(
                "Press",
                (
                    Template('-site:{primary:raw} "{primary:raw}" presse OR communiqué'),
                    Template('"{primary:raw}" intitle:interview OR intitle:article'),
                    Template('{company} "{primary:raw}" actualités', requires=("company",)),
                ),
            ),
        ),
    )
)
