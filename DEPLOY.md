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
- `vercel.json` is configured to:
  1. Serve existing files directly.
  2. Rewrite unmatched paths to `/index.html`.
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

