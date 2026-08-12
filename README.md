# joshuaheinstein.github.io

My portfolio site, live at **https://joshuaheinstein.github.io/**

Static HTML, CSS, and JavaScript — no build step, no dependencies, no
framework, zero external requests. Open `index.html` in a browser and it works.

```
index.html                  the whole page
deck.html                   standalone interview deck (present / print to PDF)
assets/css/styles.css       all styling, light + dark themes
assets/js/main.js           mode toggle, theme toggle, scroll behaviour
assets/img/                 project photos (see the README in there)
assets/resume/              both résumé PDFs, offered as downloads
.nojekyll                   tells GitHub Pages to serve files as-is
```

This repository is public, and everything in it is visible to anyone —
including the résumé PDFs. Private career material lives in a separate
private repo, not here.

## The positioning toggle

The segmented control in the top-right has three states:

- **Engineering** — leads with FPGA, RISC-V, firmware, CAN bus, hardware bring-up.
- **Leadership** — leads with cross-functional leadership, root-cause analysis,
  project management, quantitative analysis.
- **Deep-dive** — replaces the page with the interview deck: three projects in
  detail, with block diagrams, laid out to scroll through.

Engineering and Leadership are two framings of the *same* page — both versions
of every headline, summary, and bullet are present in `index.html`, tagged
`m-tech` or `m-gen`, and CSS shows one set while hiding the other. Deep-dive is
different in kind: it hides the normal sections and shows `#deck` instead.

JavaScript only flips a class on `<html>` and remembers the choice in
`localStorage`. Two consequences worth knowing:

1. **It works without JavaScript** — the page defaults to the Engineering framing.
2. **Search engines and recruiter scrapers see all the text**, in all three
   modes, because none of it is generated at runtime.

Project cards also reorder between modes — see the `.mode-general #p-*` rules
near the end of the projects section in `styles.css`.

### If you change the toggle

The sliding thumb is exactly one third of the track and moves by its own width
per step, so **all three buttons must be the same width**. `min-width` on
`.mode-btn` is the floor that guarantees that, and it must exceed the natural
width of the *longest* label — currently "Engineering" (96px desktop, 90px
under 560px). Change a label and you have to re-measure. Adding or removing a
button means redoing the thumb's `width: calc(33.3333% - 2px)` and its
`translateX` steps; the two numbers are `100/n` percent and `6/n` px.

## The deck

`deck.html` is a standalone version of the same three projects, built to
present from: arrow keys to advance, `N` for speaker notes, `Cmd/Ctrl+P` for a
10-page PDF. The Deep-dive tab and `deck.html` carry the same content in two
layouts — one to read by scrolling, one to project — so **a content change
needs making in both**.

## Editing content

Everything is in `index.html`, in plain HTML, in the order it appears on
screen. To change a bullet, find it and change it. The pattern for anything
that differs between the two modes:

```html
<span class="m-tech">What an embedded team should read</span>
<span class="m-gen">What a systems team should read</span>
```

Elements marked `class="tech-only"` appear only in embedded mode.

## Adding project photos

Drop files into `assets/img/` using the filenames listed in
[`assets/img/README.md`](assets/img/README.md). Missing images fall back to a
styled placeholder automatically, so the site never looks broken while you
fill them in one at a time.

## Accessibility

All 18 text/background colour pairs across both themes were checked against
WCAG AA (4.5:1) by computing relative luminance directly; every pair passes.
If you change a colour in `styles.css`, re-check it — `--fg-dim` in light mode
in particular sits close to the threshold on `--bg-sunken` (4.66:1).

The page also respects `prefers-reduced-motion` and `prefers-color-scheme`,
with a manual theme override.

## Local preview

Double-clicking `index.html` works. If you'd rather serve it:

```sh
python3 -m http.server 8000
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

## Still to fill in

- `assets/img/` — project photos.
- LinkedIn and GitHub URLs in the contact section. Both are marked
  `data-needs-url` in `index.html`; they render greyed out and unclickable
  until a real `href` replaces the `#`, so no dead links ship in the meantime.
