<img src="pharmakaksha_logo.jpeg" width="120" align="right" alt="Pharmakaksha logo">

# learn.pharmakaksha.com

Practice notebooks for the Pharmakaksha B.Pharm (PCI NEP 2020) courses.
Students open **https://learn.pharmakaksha.com** and run Python in their browser. They don't need a login or any installation.

**Pharmakaksha · Learn · Grow · Achieve**

## What's inside

| Folder | Course | Notebooks |
| --- | --- | --- |
| `content/BP101T Basics of Python Programming for Pharmaceutical Sciences (Theory)` | BP101T, Semester I | Units I–V (Units III–V create their practice datasets inside the notebook) |
| `content/BP201T Applied Biostatistics and Data Analytics for Pharmaceutical Sciences (Theory)` | BP201T, Semester II | Units I–V, with 6 practice datasets |
| `content/BP301T Introduction to Machine Learning in Pharmaceutical Sciences (Theory)` | BP301T, Semester III | Units I–V, with 7 practice datasets |
| `content/BP604T AI applications in Pharmaceutical Sciences (Theory)` | BP604T, Semester VI | Units I–V, with 22 practice datasets |
| `content/BP701T Biostatistics and Research Methodology (Theory)` | BP701T, Semester VII | Units I, II, III, IV A, IV B and V, with 1 practice dataset |
| `content/BP703T AI in Clinical Applications (Theory)` | BP703T, Semester VII | Units I–V, with 14 practice datasets |
| `content/BP801T Ethical Considerations and Translational Applications of AI in Pharmacy (Theory)` | BP801T, Semester VIII | Units I–V, with 12 practice datasets |

These are the materials prepared so far. Students only see the ones that have been released (see [Releasing materials](#releasing-materials)).

The site is built with [JupyterLite](https://jupyterlite.readthedocs.io). Python runs inside each student's browser, using the Pyodide engine, so there are no server costs and no limit on how many students can use it. NumPy, Pandas, Matplotlib, SciPy, statsmodels and scikit-learn are all available.

## Home page

The site opens on a Pharmakaksha home page, with the logo, the "Learn · Grow · Achieve" tagline and links to Instagram, Facebook, WhatsApp, Telegram and YouTube. Below that there is one card per course:

- A course with released notebooks lists its units. Each unit links straight to its notebook.
- A course with nothing released yet shows a **Coming soon** card.

The cards are rebuilt on every deploy from what is in `content/`, so the home page never needs editing when you release a unit. To change the wording, the social links or the styling, edit `branding/home.html`.

## Releasing materials

Materials are released one at a time. Every file in `content/` that is not released yet is listed in `.gitignore`, so git leaves it out and it never reaches the site.

To release a notebook:

1. Delete its line from `.gitignore`. Also delete the lines for the datasets (CSV files) it reads.
2. Add the files, then commit and push to `main`:
   ```bash
   git add .gitignore "content/<folder>/<notebook>.ipynb" "content/<folder>/<dataset>.csv"
   git commit -m "Release BP101T Unit II"
   git push
   ```
3. The **Build and deploy** GitHub Action rebuilds the site. The notebook is live, and on its course card, in about 2 minutes.

To add a new notebook, put the `.ipynb` file in the right course folder under `content/`, for example `content/BP101T Basics of Python Programming for Pharmaceutical Sciences (Theory)/`. Name it like the others (`BP101T_Unit2_Control_Structures_and_Functions.ipynb`), because the home page builds the unit label and title from the file name. Then either release it as above, or add its path to `.gitignore` to hold it back.

Datasets (CSV files) go next to the notebook that uses them. The notebook can then read them with `pd.read_csv("drugs.csv")`.

To add a new course, create its folder under `content/`, then add the folder name to the `COURSES` list near the top of `branding/build_home.py`. Its card then shows **Coming soon** until the first notebook is released.

Files that were committed before they were added to `.gitignore` stay published. To pull one back, run `git rm --cached "<file>"`, then commit and push. Earlier versions are still in the repository's history.

## One-time setup

1. **Create the repository.** On GitHub, create a **public** repository (this one is `ajreddys/learn-pharmakaksha-site`). Push this folder to it:
   ```bash
   git init -b main
   git add .
   git commit -m "Pharmakaksha learn site"
   git remote add origin https://github.com/ajreddys/learn-pharmakaksha-site.git
   git push -u origin main
   ```
2. **Turn on Pages.** In the repository, go to **Settings → Pages** and set **Source = GitHub Actions**.
3. **Add the DNS record.** At your domain provider for pharmakaksha.com, add one record:
   - Type: `CNAME`
   - Name / Host: `learn`
   - Value / Points to: `ajreddys.github.io`
4. **Connect the domain.** Back in **Settings → Pages**, enter `learn.pharmakaksha.com` as the **Custom domain** and save. Once the DNS check passes, tick **Enforce HTTPS**. This can take up to an hour.

## Sharing a notebook link

Links to notebooks must write spaces as `%20` and brackets as `%28` and `%29`. For example:

- Site: `https://learn.pharmakaksha.com/notebooks/index.html?path=<folder>/<notebook>.ipynb`
- Colab: `https://colab.research.google.com/github/ajreddys/learn-pharmakaksha-site/blob/main/content/<folder>/<notebook>.ipynb`

## Local preview (optional)

```bash
pip install -r requirements.txt
jupyter lite build
python branding/build_home.py
python -m http.server 8000 --directory dist
```

Then open http://localhost:8000.

## Files

| File | Purpose |
| --- | --- |
| `content/` | The notebooks and datasets students see |
| `.gitignore` | Build leftovers, plus every material in `content/` that has not been released yet |
| `jupyter_lite_config.json` | Build settings. It also adds the `comm` package, which `input()` needs in the browser |
| `jupyter-lite.json` | Site name and default Python kernel |
| `overrides.json` | Shows every cell of long notebooks at once, for smoother scrolling on phones |
| `requirements.txt` | JupyterLite versions used for the build |
| `branding/` | The Pharmakaksha home page (`home.html`) with the social links, the web-sized logo and favicon, and `build_home.py`, which holds the course list and fills in the course cards at build time. `analytics.html` holds the Cloudflare Web Analytics snippet, which the build adds to every page |
| `CNAME` | The custom domain `learn.pharmakaksha.com` |
| `.github/workflows/deploy.yml` | Builds and publishes the site on every push |
