# Deploy Guide (GitHub + Vercel)

This repo is configured for static hosting with a Vercel rewrite fallback in `vercel.json`.

## 1) Connect GitHub repository to Vercel
1. In Vercel, click **Add New Project**.
2. Import this GitHub repository.
3. Use these settings:
   - **Framework Preset**: `Other`
   - **Build Command**: *(leave empty)*
   - **Output Directory**: *(leave empty)*
   - **Install Command**: *(leave empty)*
   - **Root Directory**: repository root (`.`)
4. Click **Deploy**.

## 2) Confirm production branch
- In Vercel Project Settings → **Git**, set **Production Branch** to your main branch (commonly `main`).

## 3) Why this resolves 404s
- `vercel.json` is configured with a catch-all rewrite to `/index.html` for any route path.
- This prevents Vercel `404: NOT_FOUND` for direct visits to non-root routes.

## 4) Local verification
```bash
python3 -m http.server 4173
# open http://127.0.0.1:4173/index.html
```

## 5) Optional CLI deploy
If you want CLI deploys from your machine:
```bash
npm i -g vercel
vercel login
vercel --prod
```


## 6) Fallback page for static hosts
- `404.html` is intentionally a copy of `index.html` to support SPA fallback behavior on hosts that serve a static 404 document.


## 7) If you still see `404: NOT_FOUND`
- In Vercel, open **Project → Deployments** and verify there is a recent successful deployment from your latest commit.
- In **Project Settings → General**, confirm **Root Directory** is `.` (repo root).
- In **Project Settings → Domains**, ensure your custom domain is assigned to this project (not another Vercel project).
- If the latest commit is not deployed, trigger **Redeploy** from the newest deployment or run `vercel --prod` from an authenticated machine.
