"""Mode `username`: search for a username on public sources."""

from dorkint.builder import Category, Mode, Template, register

_SOCIAL = (
    "github.com", "x.com", "twitter.com", "instagram.com",
    "tiktok.com", "reddit.com", "youtube.com", "linkedin.com", "twitch.tv",
)

register(Mode(
    name="username",
    refinements=("city", "company"),
    categories=(
        Category("Social network profiles", (
            *(Template(f"site:{site} {{primary}}") for site in _SOCIAL),
            Template("site:linkedin.com/in {primary} {city}", requires=("city",)),
            Template("site:linkedin.com/in {primary} {company}", requires=("company",)),
            Template("site:instagram.com {primary} {city}", requires=("city",)),
        )),
        Category("Forums and communities", (
            Template("site:stackoverflow.com/users {primary}"),
            Template("site:forum.ubuntu-fr.org {primary}"),
            Template("site:commentcamarche.net {primary}"),
            Template("site:jeuxvideo.com {primary}"),
            Template("{primary} forum inurl:profil site:.fr"),
            Template("{primary} forum {city}", requires=("city",)),
        )),
        Category("Code and repositories", (
            Template("site:github.com {primary} -inurl:blob"),
            Template("site:gitlab.com {primary}"),
            Template("site:pastebin.com {primary}"),
            Template("site:dev.to {primary}"),
            Template("site:github.com {primary} {company}", requires=("company",)),
        )),
        Category("Portfolios and blogs", (
            Template("{primary} portfolio"),
            Template("{primary} blog auteur"),
            Template("site:medium.com {primary}"),
            Template("site:over-blog.com {primary}"),
            Template("{primary} portfolio {city}", requires=("city",)),
            Template("{primary} blog {company}", requires=("company",)),
        )),
        Category("Mentions in PDFs", (
            Template("filetype:pdf {primary}"),
            Template("filetype:pdf {primary} site:.fr"),
            Template("filetype:pdf {primary} {city}", requires=("city",)),
            Template("filetype:pdf {primary} {company}", requires=("company",)),
            Template("filetype:pdf {primary} {city} {company}", requires=("city", "company")),
        )),
        Category("Press mentions", (
            Template("{primary} site:lemonde.fr"),
            Template("{primary} site:lefigaro.fr"),
            Template("{primary} site:ouest-france.fr"),
            Template("{primary} actualités site:.fr"),
            Template("{primary} {city} site:.fr", requires=("city",)),
            Template("{primary} {company} site:.fr", requires=("company",)),
        )),
    ),
))
