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
    folders = sorted(p for p in CONTENT.iterdir() if p.is_dir())
    for i, folder in enumerate(f for f in folders if any(f.glob("*.ipynb"))):
        code, title, sem = course_info(folder)
        accent, accent_light = ACCENTS[i % len(ACCENTS)]
        units = []
        for nb in sorted(folder.glob("*.ipynb")):
            label, name = unit_info(nb)
            units.append(
                f'<li><a href="notebooks/index.html?path={link(nb)}">'
                f'<span class="unit">{html.escape(label)}</span>'
                f"<span>{html.escape(name)}</span></a></li>"
            )
        datasets = len(list(folder.glob("*.csv")))
        count = f"{len(units)} unit{'s' if len(units) != 1 else ''}"
        if datasets:
            count += f" · {datasets} practice dataset{'s' if datasets != 1 else ''}"
        cards.append(
            f'<article class="course" style="--accent:{accent};--accent-light:{accent_light}">'
            f'<div class="meta"><span class="code">{html.escape(code)}</span>'
            + (f"<span>Semester {sem}</span>" if sem else "")
            + f"</div><h3>{html.escape(title)}</h3><ul>{''.join(units)}</ul>"
            f'<div class="files">{count}</div>'
            "</article>"
        )
    if not cards:
        return '<div class="empty">The first course materials are coming soon.</div>'
    return '<div class="courses">' + "\n".join(cards) + "</div>"


def main():
    page = (HERE / "home.html").read_text(encoding="utf-8")
    page = page.replace("<!-- COURSES -->", render_courses())
    (DIST / "index.html").write_text(page, encoding="utf-8")
    (DIST / "branding").mkdir(exist_ok=True)
    for name in ("logo.jpg", "favicon.png"):
        shutil.copy(HERE / name, DIST / "branding" / name)
    print("Wrote branded home page to", DIST / "index.html")


if __name__ == "__main__":
    main()
