# portfolio
Portfolio Website

Latest deployed file: `index.html` (synced from `michael-leng-timeline-v4 (8).html`).

## Vercel deployment notes
- `vercel.json` is configured with a catch-all rewrite so any unmatched route resolves to `index.html`.
- This prevents Vercel `404: NOT_FOUND` on direct visits to non-root URLs. A `404.html` fallback is also included for static hosts that use a dedicated 404 page.


Deployment setup steps: see `DEPLOY.md`.
