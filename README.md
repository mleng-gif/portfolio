# portfolio

Personal portfolio website built as a single static HTML file.

## Quick start

1. Open the repo:
   ```bash
   cd /workspace/portfolio
   ```
2. Start a local static server:
   ```bash
   python3 -m http.server 8080
   ```
3. Open your browser at:
   ```
   http://localhost:8080
   ```

`index.html` is the main entry point used by static hosts (GitHub Pages, Netlify, Vercel static deploys, etc.).

## Project files

- `index.html` — website entry page currently deployed.
- `michael-leng-timeline-v3 (1).html` — older source snapshot kept for reference.
- `scripts/update_latest_html.sh` — helper script to swap in your newest HTML and back up the old `index.html`.
- `versions/` — automatic backups created when updating `index.html`.

## Update to your latest website iteration

If you have a newer HTML export, you can replace the live entry file in one command:

```bash
./scripts/update_latest_html.sh "/path/to/your/latest-file.html"
```

What this does:
- Backs up the current `index.html` into `versions/index-<timestamp>.html`
- Replaces `index.html` with your latest file

Then test it locally:

```bash
python3 -m http.server 8080
```

## Make it public for free on Vercel

Yes — this project is perfect for Vercel’s free **Hobby** tier.

### Option A (easiest): Deploy from GitHub

1. Push this repo to GitHub.
2. Go to [vercel.com](https://vercel.com) and sign in.
3. Click **Add New → Project**.
4. Import your GitHub repo.
5. Leave build settings as default (no framework / static site is fine).
6. Click **Deploy**.

Your site will be live at a URL like:
`https://your-project-name.vercel.app`

Every new push to your main branch will auto-redeploy.

### Option B: Deploy with Vercel CLI

```bash
npm i -g vercel
cd /workspace/portfolio
vercel
```

- First run: answer prompts and choose this project directory.
- To deploy production updates later:

```bash
vercel --prod
```

## Deploy notes

- Vercel automatically serves `index.html` at `/`.
- You can connect a custom domain in Vercel project settings later.
