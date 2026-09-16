# Deploying NegotiAI — GitHub + Free Public URL

Two parts: (A) get the code on GitHub so you can share a repo link,
(B) deploy it so judges can open a live URL. Part A takes ~5 minutes.
Part B takes ~15 and is optional but worth it.

---

## Part A — Push to GitHub

### 1. Create the repo (in your browser)
Go to https://github.com/new
- Repository name: `negotiai`
- Description: `Autonomous agent-to-agent negotiation system for consumer rights — TSM TECHNOVA 2026`
- Public
- Do **not** tick "Add a README" (you already have one)
- Click **Create repository**

### 2. Push from your Mac

```bash
cd ~/negotiai

git init
git add .
git commit -m "NegotiAI — autonomous agent-to-agent negotiation engine"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/negotiai.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

If it asks for a password, GitHub no longer accepts your account password over
HTTPS — you need a Personal Access Token instead:
https://github.com/settings/tokens → "Generate new token (classic)" → tick
`repo` scope → copy the token → paste it as the password when prompted.

### 3. Confirm
Refresh your repo page. You should see all files, with the README rendering
on the front page. **That link is what you share with judges.**

Note: `.gitignore` deliberately excludes `venv/` and `*.db`, so your virtual
environment and local demo database don't get committed. Anyone cloning runs
`pip install -r requirements.txt` and gets a clean setup.

---

## Part B — Deploy a live public URL (free)

### B1. Backend on Render

1. Go to https://render.com and sign up with your GitHub account.
2. Click **New** → **Blueprint**.
3. Select your `negotiai` repo. Render reads `render.yaml` automatically and
   fills in the build and start commands.
4. Click **Apply**. First build takes ~3-5 minutes.
5. When it finishes you get a URL like `https://negotiai-backend.onrender.com`.
   Test it: open `https://negotiai-backend.onrender.com/api/health` — you
   should see `{"status":"ok","llm_mode":false}`.

**Important free-tier caveat:** Render's free instances sleep after ~15 minutes
of inactivity, and the next request takes ~30-50 seconds to wake it. If you're
demoing live, open the URL a minute beforehand to wake it up. Also, the SQLite
database resets whenever the instance restarts — fine for a demo, but be
honest about it if a judge asks about persistence; the real answer is
"SQLite for the demo, Postgres for production, one connection-string change."

### B2. Point the frontend at your deployed backend

Open `frontend/index.html`, find this line near the top of the `<script>`:

```js
: "https://YOUR-DEPLOYED-BACKEND-URL";
```

Replace it with your actual Render URL (no trailing slash):

```js
: "https://negotiai-backend.onrender.com";
```

Commit and push:

```bash
git add frontend/index.html
git commit -m "Point frontend at deployed backend"
git push
```

The local-development path still works untouched — the code auto-detects
localhost and uses `http://localhost:8000` when you're running locally.

### B3. Frontend on GitHub Pages (simplest, no new account)

```bash
cd ~/negotiai
git subtree push --prefix frontend origin gh-pages
```

Then in your repo: **Settings** → **Pages** → Source: `gh-pages` branch → Save.
After a minute your site is live at
`https://YOUR-USERNAME.github.io/negotiai/`

**Alternative — Netlify** (nicer URL, drag-and-drop): go to
https://app.netlify.com/drop and drag your `frontend` folder onto the page.
Instant URL, no CLI.

### B4. CORS check
`backend/main.py` currently allows all origins (`allow_origins=["*"]`), so
your deployed frontend can call your deployed backend with no extra config.
Before any real production use you'd narrow this to your actual frontend
domain — worth mentioning to judges as something you're aware of rather than
something you missed.

---

## What to tell judges

- **Repo:** `https://github.com/YOUR-USERNAME/negotiai`
- **Live demo:** your GitHub Pages / Netlify URL
- **Runs locally in 3 commands** — `pip install -r requirements.txt`, then
  `uvicorn backend.main:app --port 8000`, then open `frontend/index.html`
- **Zero API keys required** — the engine runs fully offline; LLM paraphrasing
  is an optional enhancement layer, not a dependency
