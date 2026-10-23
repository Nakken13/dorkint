"""Mode `username` : recherche d'un pseudo sur des sources publiques."""

from dorkint.builder import Category, Mode, Template, register

_SOCIAL = (
    "github.com", "x.com", "twitter.com", "instagram.com",
    "tiktok.com", "reddit.com", "youtube.com", "linkedin.com", "twitch.tv",
)

register(Mode(
    name="username",
    refinements=("city", "company"),
    categories=(
        Category("Profils réseaux sociaux", (
            *(Template(f"site:{site} {{principal}}") for site in _SOCIAL),
            Template("site:linkedin.com/in {principal} {city}", requires=("city",)),
            Template("site:linkedin.com/in {principal} {company}", requires=("company",)),
            Template("site:instagram.com {principal} {city}", requires=("city",)),
        )),
        Category("Forums et communautés", (
            Template("site:stackoverflow.com/users {principal}"),
            Template("site:forum.ubuntu-fr.org {principal}"),
            Template("site:commentcamarche.net {principal}"),
            Template("site:jeuxvideo.com {principal}"),
            Template("{principal} forum inurl:profil site:.fr"),
            Template("{principal} forum {city}", requires=("city",)),
        )),
        Category("Code et dépôts", (
            Template("site:github.com {principal} -inurl:blob"),
            Template("site:gitlab.com {principal}"),
            Template("site:pastebin.com {principal}"),
            Template("site:dev.to {principal}"),
            Template("site:github.com {principal} {company}", requires=("company",)),
        )),
        Category("Portfolios et blogs", (
            Template("{principal} portfolio"),
            Template("{principal} blog auteur"),
            Template("site:medium.com {principal}"),
            Template("site:over-blog.com {principal}"),
            Template("{principal} portfolio {city}", requires=("city",)),
            Template("{principal} blog {company}", requires=("company",)),
        )),
        Category("Mentions dans des PDF", (
            Template("filetype:pdf {principal}"),
            Template("filetype:pdf {principal} site:.fr"),
            Template("filetype:pdf {principal} {city}", requires=("city",)),
            Template("filetype:pdf {principal} {company}", requires=("company",)),
            Template("filetype:pdf {principal} {city} {company}", requires=("city", "company")),
        )),
        Category("Mentions presse", (
            Template("{principal} site:lemonde.fr"),
            Template("{principal} site:lefigaro.fr"),
            Template("{principal} site:ouest-france.fr"),
            Template("{principal} actualités site:.fr"),
            Template("{principal} {city} site:.fr", requires=("city",)),
            Template("{principal} {company} site:.fr", requires=("company",)),
        )),
    ),
))
