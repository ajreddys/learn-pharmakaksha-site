<img src="pharmakaksha_logo.jpeg" width="120" align="right" alt="Pharmakaksha logo">

# learn.pharmakaksha.com

Practice notebooks for the Pharmakaksha B.Pharm (PCI NEP 2020) courses.
Students open **https://learn.pharmakaksha.com** and run Python in their browser. They don't need a login or any installation.

**Pharmakaksha · Learn · Grow · Achieve**

## What's inside

| Folder | Course | Notebooks |
| --- | --- | --- |
| `content/BP101T Basics of Python Programming for Pharmaceutical Sciences (Theory)` | BP101T, Semester I | Unit I |
| `content/BP301T Introduction to Machine Learning in Pharmaceutical Sciences (Theory)` | BP301T, Semester III | Units I–V, with 7 practice datasets |

The site is built with [JupyterLite](https://jupyterlite.readthedocs.io). Python runs inside each student's browser, using the Pyodide engine, so there are no server costs and no limit on how many students can use it. NumPy, Pandas, Matplotlib, SciPy, statsmodels and scikit-learn are all available.

## Adding a notebook

1. Put the `.ipynb` file in the right course folder under `content/`, for example `content/BP101T Basics of Python Programming for Pharmaceutical Sciences (Theory)/`.
2. Commit and push to `main`.
3. The **Build and deploy** GitHub Action rebuilds the site. The notebook is live in about 2 minutes.

Datasets (CSV files) go next to the notebook that uses them. The notebook can then read them with `pd.read_csv("drugs.csv")`.

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
python -m http.server 8000 --directory dist
```

Then open http://localhost:8000.

## Files

| File | Purpose |
| --- | --- |
| `content/` | The notebooks and datasets students see |
| `jupyter_lite_config.json` | Build settings. It also adds the `comm` package, which `input()` needs in the browser |
| `jupyter-lite.json` | Site name. It also makes the site open directly on the notebook list |
| `overrides.json` | Shows every cell of long notebooks at once, for smoother scrolling on phones |
| `requirements.txt` | JupyterLite versions used for the build |
| `CNAME` | The custom domain `learn.pharmakaksha.com` |
| `.github/workflows/deploy.yml` | Builds and publishes the site on every push |
