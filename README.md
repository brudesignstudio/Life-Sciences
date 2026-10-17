# Life Sciences Desk

**Push `index.html`.** It's the complete page and works on any website or opened straight from your computer. It's the only file the site needs; the logo icons are built into it.

| File | What it is |
|---|---|
| `index.html` | The working page. Upload this. |
| `src/app.html` | The copy that gets edited, and the source for the claude.ai version. Don't upload it; it doesn't work on its own. |
| `src/build.py` | Rebuilds `index.html` from `src/app.html`. |
| `assets/` | Your logo (`Life Sciences Logo.png`, used in the page header) and favicon (`Life Sciences favicon.png`), plus transparent versions of each. The page has its own copies built in, so the site doesn't need this folder. |

After any change to `src/app.html`, rebuild the working page:

```bash
python3 src/build.py
```

## Putting it on GitHub Pages

1. Push this folder to a GitHub repository, with `index.html` at the top level.
2. In the repository, go to **Settings → Pages**, set **Source** to *Deploy from a branch*, pick `main` and `/ (root)`, and save.
3. After a minute or two the page is live at `https://<your-username>.github.io/<repo-name>/`.

After rebuilding `index.html`, commit and push it again to update the live page.
