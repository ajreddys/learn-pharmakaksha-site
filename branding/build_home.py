"""Write the branded home page into dist/ after `jupyter lite build`.

The course list is built from whatever is in content/ at build time, so a
course or unit appears on the home page as soon as its notebook is published.
"""

import html
import re
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
DIST = ROOT / "dist"
HERE = Path(__file__).resolve().parent

# (accent, lighter accent for dark mode), taken from the logo's medallions
ACCENTS = [
    ("#2b4f8c", "#8fb0e8"),  # navy
    ("#6f3a96", "#c7a4e6"),  # purple
    ("#3f6b2a", "#9fcd84"),  # green
    ("#1f6f6f", "#7fcfcf"),  # teal
    ("#a4284a", "#f093ab"),  # crimson
    ("#9a7420", "#e2c27a"),  # gold
]
ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

# Every course gets a card on the home page, even before any of its notebooks
# are published (it shows "Coming soon" until then). Use the course's folder
# name under content/. A folder in content/ that is missing here still gets a card.
COURSES = [
    "BP101T Basics of Python Programming for Pharmaceutical Sciences (Theory)",
    "BP201T Applied Biostatistics and Data Analytics for Pharmaceutical Sciences (Theory)",
    "BP301T Introduction to Machine Learning in Pharmaceutical Sciences (Theory)",
    "BP604T AI applications in Pharmaceutical Sciences (Theory)",
    "BP701T Biostatistics and Research Methodology (Theory)",
    "BP703T AI in Clinical Applications (Theory)",
    "BP801T Ethical Considerations and Translational Applications of AI in Pharmacy (Theory)",
]


def course_info(folder):
    """'BP604T AI applications in ... (Theory)' -> ('BP604T', 'AI applications in ...', 'VI')"""
    code, _, title = folder.name.partition(" ")
    title = re.sub(r"\s*\((Theory|Practical)\)\s*$", "", title)
    sem = re.match(r"BP(\d)", code)
    return code, title, ROMAN[int(sem.group(1))] if sem else ""


def unit_info(nb):
    """'BP701T_Unit4A_Estimation_and_t_Tests' -> ('Unit IV A', 'Estimation and t Tests')"""
    m = re.match(r"[A-Z]+\d+[A-Z]?_Unit(\d+)([A-Z]?)_(.+)", nb.stem)
    if not m:
        return "", nb.stem.replace("_", " ")
    num, part, name = m.groups()
    label = f"Unit {ROMAN[int(num)]}" + (f" {part}" if part else "")
    return label, name.replace("_", " ")


def link(path):
    return quote(path.relative_to(CONTENT).as_posix(), safe="/")


def render_courses():
    cards = []
    names = set(COURSES)
    if CONTENT.is_dir():
        names |= {p.name for p in CONTENT.iterdir() if p.is_dir()}
    # sorting by name keeps each course's colour fixed as units are released
    for i, folder in enumerate(CONTENT / n for n in sorted(names)):
        code, title, sem = course_info(folder)
        accent, accent_light = ACCENTS[i % len(ACCENTS)]
        meta = (
            f'<div class="meta"><span class="code">{html.escape(code)}</span>'
            + (f"<span>Semester {sem}</span>" if sem else "")
            + "</div>"
        )
        if not any(folder.glob("*.ipynb")):
            cards.append(
                f'<article class="course soon" style="--accent:{accent};--accent-light:{accent_light}">'
                f"{meta}<h3>{html.escape(title)}</h3>"
                '<p class="soon-note">Notebooks for this course are on the way.</p>'
                '<div class="files"><span class="soon-tag">Coming soon</span></div>'
                "</article>"
            )
            continue
        units = []
        for nb in sorted(folder.glob("*.ipynb")):
            label, name = unit_info(nb)
            units.append(
                f'<li><a href="notebooks/index.html?path={link(nb)}" target="_blank" rel="noopener">'
                f'<span class="unit">{html.escape(label)}</span>'
                f"<span>{html.escape(name)}</span></a></li>"
            )
        datasets = len(list(folder.glob("*.csv")))
        count = f"{len(units)} unit{'s' if len(units) != 1 else ''}"
        if datasets:
            count += f" · {datasets} practice dataset{'s' if datasets != 1 else ''}"
        cards.append(
            f'<article class="course" style="--accent:{accent};--accent-light:{accent_light}">'
            f"{meta}<h3>{html.escape(title)}</h3><ul>{''.join(units)}</ul>"
            f'<div class="files">{count}</div>'
            "</article>"
        )
    return '<div class="courses">' + "\n".join(cards) + "</div>"


def main():
    page = (HERE / "home.html").read_text(encoding="utf-8")
    page = page.replace("<!-- COURSES -->", render_courses())
    (DIST / "index.html").write_text(page, encoding="utf-8")
    (DIST / "branding").mkdir(exist_ok=True)
    for name in ("logo.jpg", "favicon.png", "apple-touch-icon.png"):
        shutil.copy(HERE / name, DIST / "branding" / name)
    # JupyterLite pages use their own .ico files (and swap to "busy" ones while
    # Python runs), so replace them all with the Pharmakaksha logo.
    for ico in [*DIST.glob("*/favicon.ico"), *DIST.glob("static/favicons/*.ico")]:
        shutil.copy(HERE / "favicon.ico", ico)
    # Cloudflare Web Analytics on the home page and every JupyterLite page
    snippet = (HERE / "analytics.html").read_text(encoding="utf-8").strip()
    for page_file in [DIST / "index.html", *DIST.glob("*/index.html")]:
        text = page_file.read_text(encoding="utf-8")
        if "cloudflareinsights" not in text and "</body>" in text:
            page_file.write_text(text.replace("</body>", snippet + "\n</body>", 1), encoding="utf-8")
    print("Wrote branded home page to", DIST / "index.html")


if __name__ == "__main__":
    main()
