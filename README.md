# joshuaheinstein.github.io

My portfolio site, live at **https://joshuaheinstein.github.io/**

Static HTML, CSS, and JavaScript — no build step, no dependencies, no
framework, zero external requests. Open `index.html` in a browser and it works.

```
index.html                  the whole page
assets/css/styles.css       all styling, light + dark themes
assets/js/main.js           mode toggle, theme toggle, scroll behaviour
assets/img/                 project photos (see the README in there)
assets/resume/              both résumé PDFs, offered as downloads
tools/                      contrast + layout checkers
.nojekyll                   tells GitHub Pages to serve files as-is
```

This repository is public, and everything in it is visible to anyone —
including the résumé PDFs. Private career material lives in a separate
private repo, not here.

## The positioning toggle

The site carries two framings of the same career, switched by the segmented
control in the top-right:

- **Engineering** — leads with FPGA, RISC-V, firmware, CAN bus, hardware bring-up.
- **Leadership** — leads with cross-functional leadership, root-cause analysis,
  project management, quantitative analysis.

Both versions of every headline, summary, and bullet list are present in
`index.html`, tagged `m-tech` or `m-gen`. CSS shows one set and hides the
other; JavaScript only flips a class on `<html>` and remembers the choice in
`localStorage`. Two consequences worth knowing:

1. **It works without JavaScript** — the page renders fully and defaults to the
   engineering framing. The scroll-reveal styles are scoped to a `.js` class set
   before first paint, precisely so that stays true.
2. **Search engines and recruiter scrapers see all the text**, because none of
   it is generated at runtime.

Project cards also reorder between modes — see the `.mode-general #p-*` rules
near the end of `styles.css`.

## Editing content

Everything is in `index.html`, in plain HTML, in the order it appears on
screen. To change a bullet, find it and change it. The pattern for anything
that differs between the two modes:

```html
<span class="m-tech">What an embedded team should read</span>
<span class="m-gen">What a systems team should read</span>
```

Elements marked `class="tech-only"` appear only in engineering mode.

## Adding project photos

Drop files into `assets/img/` using the filenames listed in
[`assets/img/README.md`](assets/img/README.md). Missing images fall back to a
styled placeholder automatically, so the site never looks broken while you
fill them in one at a time. Two placeholders remain.

## Checking your changes

There are no unit tests. Two scripts do the checking, and both exit non-zero on
failure:

```sh
python tools/check-contrast.py   # every colour pair vs WCAG AA
python tools/check-layout.py     # toggle widths, overflow, images
```

Run both after touching colours, type size, or the toggle labels — each of the
site's known failure modes was caught by these rather than by eye. The layout
checker needs Chromium:

```sh
pip install playwright && python -m playwright install chromium
```

## Accessibility

All 42 text/background colour pairs across both themes are checked against
WCAG AA (4.5:1) by computing relative luminance directly; every pair passes,
with the tightest at 4.82:1. If you change a colour in `styles.css`, re-run
`tools/check-contrast.py` — two pairs failed the first time the warm palette
was tried, and neither was obvious by eye.

The page also respects `prefers-reduced-motion` and `prefers-color-scheme`,
with a manual theme override, and prints cleanly.

## Local preview

Double-clicking `index.html` works. If you'd rather serve it:

```sh
python -m http.server 8000
# then open http://localhost:8000
```

## Publishing

Because this repo is named `<username>.github.io`, GitHub Pages serves it
automatically from the default branch — pushing to `main` deploys. No build,
no action, no configuration.

### Custom domain

Buy a domain, add a file named `CNAME` at the repo root containing just the
domain (e.g. `joshuaheinstein.com`), point DNS at GitHub per
[their guide](https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site),
then enable *Enforce HTTPS* in Settings → Pages.

## Previous design

The earlier black/white/blue version is preserved at tag `v1-original-design`
and branch `backup/v1-original-design`:

```sh
git checkout v1-original-design
```
