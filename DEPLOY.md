# Deploying the 296 raccoon removal sites to Netlify

Each keyword (after removing 27 exact duplicates from your original 323) got its own
5-page static site in `sites/<slug>/` — `index.html`, `services.html`,
`service-area.html`, `faq.html`, `contact.html`, plus `robots.txt` and `sitemap.xml`.
Every site has its own theme/layout combination, its own copy, an embedded Google
Map for its city/county, and a floating `tel:+18339013895` call button.

This has to run from your own machine — the sandbox this was built in cannot reach
Netlify's deploy API directly (blocked by its network policy), so a local run is the
only way to actually push the content live.

## One-time setup

```bash
npm install -g netlify-cli
netlify login
```

Log in with the same Netlify account/team the sites should live under.

## Deploy everything

From the repo root:

```bash
./deploy-all.sh
```

Optional: if you want the sites under a specific team, set `NETLIFY_ACCOUNT` to that
team's slug first: `NETLIFY_ACCOUNT=your-team-slug ./deploy-all.sh`.

This creates (or reuses, if already created) one Netlify site per keyword, named
after the keyword (e.g. `raccoonremovaldallastx` → `raccoonremovaldallastx.netlify.app`),
and deploys that site's 5 pages to it. It's safe to re-run if it gets interrupted —
already-created sites are detected by name and reused rather than duplicated.

Expect it to take a while (296 sites, roughly a few seconds each) — it prints
progress as `[n/296] slug ... https://slug.netlify.app` for each one.

When it finishes, **`data/live-urls.csv`** has the final list: `keyword,slug,url`.
That's the sheet you asked for — send it back to me (or just use it directly) and
I'll turn it into a clean spreadsheet if you want.

## If a site shows a login/SSO wall instead of the page

A handful of test sites created earlier from this session (before the local-deploy
pivot) had Netlify's team visitor-access-control turned on by default. If any site
the script creates shows that instead of your page, it's a team-wide Netlify setting,
not a per-site one — turn "Visitor access control" off for the team once in the
Netlify dashboard (Team settings → Visitor access), and it applies to all sites at once.

## A few names may get a `-2`/`-3` suffix

Netlify site names are global across all Netlify users. If a plain slug like
`raccoonremovalorlandofl` happens to already be taken (by you or anyone else), the
script retries with `-2`, `-3`, etc. and records whatever name actually got used in
`data/live-urls.csv` — that file is always the source of truth for the real URLs,
not the slug list in `data/sites.json`.

## Making sites indexable

Each site already ships `robots.txt` (`Allow: /`, pointing at its `sitemap.xml`) and
a `<meta name="robots" content="index, follow">` tag plus canonical URLs on every
page, so there's nothing extra to do for basic crawlability. Netlify sites are public
and indexable by default. If you want faster initial indexing, submit each
`sitemap.xml` in Google Search Console (or Bing Webmaster Tools) — with 296 sites
that's realistically a batch job of its own, not something to do by hand one at a time.
