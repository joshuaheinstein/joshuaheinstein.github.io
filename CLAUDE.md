# Context for Claude Code

Notes for any future session working on this site. Written so a fresh session
doesn't need the original conversation re-explained.

## What this is

Joshua Heinstein's portfolio site, live at https://joshuaheinstein.github.io/.
Harvey Mudd B.S. Engineering (May 2026), based in New York City, targeting
embedded/hardware and systems/leadership roles.

## Architecture, and why

**Static HTML/CSS/JS at the repo root. No framework, no build step, no
dependencies, zero external requests.** This is deliberate, not a shortcut:

- The site must still be editable by hand in a year with no toolchain to
  restore. Don't introduce npm, a bundler, or a framework without a concrete
  reason that outweighs that.
- The system font stack (`-apple-system, BlinkMacSystemFont, …`) is a choice,
  not a default. It renders as SF Pro on Apple devices, which is where the
  Apple-like feel comes from, and costs zero network requests. A Google Fonts
  pairing (Space Grotesk + Archivo) was built and compared side by side; the
  difference was marginal and not worth the external dependency. Don't add web
  fonts without a strong reason.
- Repo is named `<username>.github.io`, so Pages deploys automatically from
  `main` on push. No workflow, no configuration.

Private career material (notes, salary research) belongs in the separate
private `Career` repo, never here — everything in this repo is public.

## The positioning toggle

The header carries a two-state segmented control: **Engineering** and
**Leadership**. Both framings of every headline, summary, and bullet exist in
`index.html`, tagged `m-tech` (Engineering) or `m-gen` (Leadership). CSS shows
one set and hides the other; `main.js` only flips a class on `<html>` and
persists the choice to `localStorage`.

Consequences to preserve:

1. The page renders fully **without JavaScript**, defaulting to Engineering.
2. **All text stays in the DOM**, so crawlers and recruiter scrapers see both
   framings. Don't move this content into JS-generated markup.

Elements marked `tech-only` appear only in Engineering mode. Project cards
reorder between modes via the `.mode-general #p-*` rules near the end of the
projects section in `styles.css`.

## Two invariants that have broken before

**1. Mode-switch buttons must be equal width.** The sliding thumb is exactly
`50%` and translates by its own width, so unequal labels misalign it. Both
buttons use a `min-width` floor that must exceed the *longer* label's natural
width (currently 96px desktop / 90px under 560px, for "Engineering" at
92.2px / 85.3px). **If you change a label, re-measure and raise the floor.**
The switch's hairline is an inset `box-shadow`, not a `border`, so the 50%
math stays exact — don't convert it to a border.

**2. Colour contrast is verified, not eyeballed.** All 18 text/background
pairs across both themes pass WCAG AA (4.5:1), checked by computing relative
luminance. `--fg-dim` in light mode (`#68686e`) is the tightest at 4.66:1 on
`--bg-sunken`, behind the inactive toggle button. **Re-check the ratio if you
change any colour** — the original `#86868b` failed at 3.33:1.

## Images

`assets/img/` — filenames documented in the README there. Missing images fall
back to a styled placeholder via an `onerror` handler on each `<img>`, so the
site never looks broken with photos missing. Real bench photos are preferred
over renders.

## Verifying changes

There are no tests. Verify visually with a headless browser rather than
assuming — this caught both invariant breaks above:

```sh
python3 -m http.server 8000    # then drive it with Playwright
```

Check at 1440px and 390px, in light and dark, in both toggle modes.

## Outstanding

- Project photos in `assets/img/` (the highest-value remaining improvement).
- GitHub profile URL in the contact section — still a `#` placeholder marked
  `data-needs-url`, rendered greyed out and unclickable until replaced.
