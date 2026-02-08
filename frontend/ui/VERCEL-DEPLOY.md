# Hosting TrendVision on Vercel

This guide walks you through deploying the **Next.js frontend** (`frontend/ui`) to Vercel from scratch: account setup, connecting the repo, configuring the build, and going live.

---

## Why Vercel for this project?

- **Made for Next.js** – Vercel builds and runs Next.js apps with zero config (SSR, API routes, edge).
- **Git-based deploys** – Push to your branch → automatic build and deploy. Preview URLs for every PR.
- **Free tier** – Enough for personal/hackathon projects (bandwidth and build minutes limits apply).
- **Global CDN** – Your app is served from edge locations for fast load times.

**What gets hosted:** Only the **Next.js app** in `frontend/ui`. Your Python backend (Django, Flask in `cam_code`, etc.) is not deployed by this flow; you’d host that elsewhere (e.g. Railway, Render, Fly.io) and point the frontend to its URL via environment variables.

---

## Prerequisites

1. **Code in a Git repository**  
   Your project should be on **GitHub**, **GitLab**, or **Bitbucket**. If it’s only local, create a repo and push:

   ```bash
   cd c:\Users\nasax\hacker\Hacklahoma2026
   git init
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

2. **Node.js**  
   Not required on your machine for “hosting,” but you need it to run `npm run build` locally and verify the app builds before deploying.

---

## Step 1: Create a Vercel account and install the CLI (optional)

1. Go to **[vercel.com](https://vercel.com)** and sign up (e.g. “Continue with GitHub”).  
2. **(Optional)** Install the Vercel CLI for deploys and logs from your terminal:

   ```bash
   npm i -g vercel
   ```

   You can do everything from the Vercel dashboard without the CLI if you prefer.

---

## Step 2: Import the project in Vercel

1. In the Vercel dashboard, click **“Add New…” → “Project”**.  
2. **Import** your Git repository (e.g. the one that contains `Hacklahoma2026`).  
   - If you don’t see the repo, use “Adjust GitHub App Permissions” and grant Vercel access to the right org/repo.  
3. You’ll see the **Configure Project** screen. This is where the only critical setting for your repo lives.

---

## Step 3: Set the Root Directory (critical for your repo)

Your Next.js app is **not** at the repo root; it’s in **`frontend/ui`**.

1. In **“Root Directory”**, click **“Edit”**.  
2. Enter:

   ```text
   frontend/ui
   ```

   If your repo root is actually **`Hacklahoma2026`** (i.e. the folder with `frontend/` is the root), then use:

   ```text
   frontend/ui
   ```

   So: **Root Directory = the path from the repo root to the folder that contains `package.json` and `next.config.mjs`.**  
   For you, that’s `frontend/ui`.

3. Leave **“Framework Preset”** as **Next.js** (Vercel will detect it from the root you just set).  
4. **Build Command:** leave as `npm run build` (or `next build`).  
5. **Output Directory:** leave as default (Next.js uses `.next`; Vercel knows this).  
6. **Install Command:** leave as `npm install`.

Then click **Deploy**. Vercel will clone the repo, run `npm install` and `npm run build` inside `frontend/ui`, and deploy the result.

---

## Step 4: Environment variables (e.g. for APIs)

If your Next.js app uses env vars (e.g. in `frontend/ui/.env.local`), you must add them in Vercel so production builds and runtime can see them.

1. In the Vercel project, go to **Settings → Environment Variables**.  
2. Add each variable:
   - **Name:** same as in `.env.local` (e.g. `NEXT_PUBLIC_API_URL`).  
   - **Value:** the value for production (e.g. your backend API URL).  
   - **Environment:** choose **Production**, **Preview**, or both.  
3. **Redeploy** after changing env vars (Deployments → … on latest → Redeploy), so the new values are baked in.

**Important:** Only variables prefixed with `NEXT_PUBLIC_` are exposed to the browser. Use unprefixed vars for server-only secrets (API keys, etc.).

---

## Step 5: After the first deploy

- **Production URL:** `https://your-project-name.vercel.app` (or a custom domain you add).  
- **Logs:** **Deployments → select a deployment → “Building” / “Functions”** for build and runtime logs.  
- **Preview deployments:** Every push to a non-production branch (and every PR) gets a unique preview URL. Production branch is usually `main` or `master` (configurable under **Settings → Git**).

---

## Step 6: Custom domain (optional)

1. **Settings → Domains.**  
2. Add your domain (e.g. `trendvision.com` or `app.trendvision.com`).  
3. Follow Vercel’s instructions to add the DNS records (A/CNAME) at your registrar.  
4. Vercel will provision SSL and serve the app on that domain.

---

## Summary checklist

| Step | Action |
|------|--------|
| 1 | Code in Git (GitHub/GitLab/Bitbucket). |
| 2 | Vercel account + (optional) CLI. |
| 3 | Import repo → set **Root Directory** to `frontend/ui`. |
| 4 | Deploy; fix any build errors using the build logs. |
| 5 | Add **Environment Variables** in Vercel and redeploy if needed. |
| 6 | (Optional) Add a **custom domain** under Settings → Domains. |

---

## Deploying from the CLI (alternative)

If you use the CLI and want to deploy from your machine:

```bash
cd c:\Users\nasax\hacker\Hacklahoma2026\frontend\ui
vercel
```

Follow the prompts; when asked for the project root, the current directory (`frontend/ui`) is correct. To deploy to production:

```bash
vercel --prod
```

Linking the CLI to the same Vercel project you created in the dashboard keeps Git-based and CLI deploys in sync.

---

## Troubleshooting

- **Build fails:** Open the deployment in Vercel → **Building** tab. Most issues are missing env vars, wrong **Root Directory**, or Node version. You can set **Node.js Version** in **Settings → General** (e.g. 20.x).  
- **404 on routes:** Ensure **Root Directory** is exactly `frontend/ui` so `next.config.mjs` and `app/` are used.  
- **Env vars not working:** They’re applied at build time; change in **Settings → Environment Variables**, then **Redeploy**.

Once the Root Directory is set to `frontend/ui` and env vars (if any) are set, hosting on Vercel is “push to Git → automatic deploy.”
