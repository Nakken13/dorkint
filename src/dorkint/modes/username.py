"""Mode `username` : recherche d'un pseudo sur des sources publiques."""

from dorkint.builder import Category, Mode, Template, register

_SOCIAL = (
    "github.com", "x.com", "twitter.com", "instagram.com",
    "tiktok.com", "reddit.com", "youtube.com", "linkedin.com", "twitch.tv",
)

register(Mode(
    name="username",
    refinements=("ville", "entreprise"),
    categories=(
        Category("Profils réseaux sociaux", (
            *(Template(f"site:{site} {{principal}}") for site in _SOCIAL),
            Template("site:linkedin.com/in {principal} {ville}", requires=("ville",)),
            Template("site:linkedin.com/in {principal} {entreprise}", requires=("entreprise",)),
            Template("site:instagram.com {principal} {ville}", requires=("ville",)),
        )),
        Category("Forums et communautés", (
            Template("site:stackoverflow.com/users {principal}"),
            Template("site:forum.ubuntu-fr.org {principal}"),
            Template("site:commentcamarche.net {principal}"),
            Template("site:jeuxvideo.com {principal}"),
            Template("{principal} forum inurl:profil site:.fr"),
            Template("{principal} forum {ville}", requires=("ville",)),
        )),
        Category("Code et dépôts", (
            Template("site:github.com {principal} -inurl:blob"),
            Template("site:gitlab.com {principal}"),
            Template("site:pastebin.com {principal}"),
            Template("site:dev.to {principal}"),
            Template("site:github.com {principal} {entreprise}", requires=("entreprise",)),
        )),
        Category("Portfolios et blogs", (
            Template("{principal} portfolio"),
            Template("{principal} blog auteur"),
            Template("site:medium.com {principal}"),
            Template("site:over-blog.com {principal}"),
            Template("{principal} portfolio {ville}", requires=("ville",)),
            Template("{principal} blog {entreprise}", requires=("entreprise",)),
        )),
        Category("Mentions dans des PDF", (
            Template("filetype:pdf {principal}"),
            Template("filetype:pdf {principal} site:.fr"),
            Template("filetype:pdf {principal} {ville}", requires=("ville",)),
            Template("filetype:pdf {principal} {entreprise}", requires=("entreprise",)),
            Template("filetype:pdf {principal} {ville} {entreprise}", requires=("ville", "entreprise")),
        )),
        Category("Mentions presse", (
            Template("{principal} site:lemonde.fr"),
            Template("{principal} site:lefigaro.fr"),
            Template("{principal} site:ouest-france.fr"),
            Template("{principal} actualités site:.fr"),
            Template("{principal} {ville} site:.fr", requires=("ville",)),
            Template("{principal} {entreprise} site:.fr", requires=("entreprise",)),
        )),
    ),
))
