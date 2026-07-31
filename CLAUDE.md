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
  not a default. It costs zero network requests. A Google Fonts pairing was
  built and compared side by side; the difference was marginal and not worth
  the external dependency. Don't add web fonts without a strong reason.
- Repo is named `<username>.github.io`, so Pages deploys automatically from
  `main` on push. No workflow, no configuration.

Private career material (notes, salary research) belongs in the separate
private `Career` repo, never here — everything in this repo is public.

## Visual direction: warm, not clinical

The site was redesigned in July 2026 away from an Apple-style pure
black/white/blue palette, which read as cold and impersonal. The current
direction is **warm ink and amber on cream**:

- Neutrals carry a deliberate warm cast (`#fdfbf6` / `#1e1913` in light,
  `#17130f` / `#f7f1e8` in dark) rather than pure white and pure black.
- The accent is amber (`--accent`, `--accent-fill`), not blue.
- Corners are large (`--r-xl: 40px` on cards) — softness carries most of the
  warmth.
- The hero uses a soft radial `--wash-a/-b` gradient. The previous design's
  cold glow and technical grid overlay are gone; don't reintroduce them.
- Every project photo is a real bench photo, not a render. That is the single
  biggest contributor to the site not feeling like a template.

The previous design is preserved at tag `v1-original-design` and branch
`backup/v1-original-design` if any of it needs to come back.

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
reorder between modes via the `.mode-general #p-*` rules near the end of
`styles.css`.

## Three invariants that have broken before

**1. Mode-switch buttons must render at equal width.** The sliding thumb is
exactly `50%` and translates by its own width, so if the `min-width` floor sits
*below* the longer label's natural width, the two buttons render at different
widths and the thumb lines up with neither. This has now broken twice — once
when the labels were renamed, once when the type size changed. Measured floors
are **108px desktop / 96px under 560px** ("Engineering" measures 103.3px and
90.6px respectively). **Changing a label or the font size means re-measuring.**
The switch's hairline is an inset `box-shadow`, not a `border`, so the 50% math
stays exact — don't convert it to a border.

**2. Colour contrast is verified, not eyeballed.** All 42 text/background pairs
across both themes pass WCAG AA (4.5:1). Two pairs failed on the first pass of
the warm palette and would have shipped if judged by eye: chip text over
`--accent-soft` on `--bg-sunken` (4.27:1) and white on the dark-mode
`--accent-fill` (3.78:1). Tightest surviving pair is 4.82:1.

**3. Scroll-reveal must not hide the page from non-JS visitors.** `.reveal`
starts at `opacity: 0`, so the rule is scoped to `.js`, which an inline script
in `<head>` sets before first paint. Before that scoping the entire page —
including the hero — was invisible with scripting disabled, silently
contradicting the no-JS promise above. Keep the `.js` scope.

## Verifying changes

There are no unit tests. Two scripts in `tools/` do the checking, and both exit
non-zero on failure:

```sh
python tools/check-contrast.py   # all 42 colour pairs vs WCAG AA
python tools/check-layout.py     # switch widths, overflow, image resolution
```

`check-layout.py` serves the site on a scratch port and drives it with headless
Chromium at 1440px and 390px in both positioning modes (needs
`pip install playwright && python -m playwright install chromium`).

Run both after any change to colours, type size, or toggle labels. They exist
because each of the invariants above was caught by measurement, not by looking.

## Images

`assets/img/` — filenames and what's still missing are documented in the README
there. Missing images fall back to a styled placeholder via an `onerror`
handler on each `<img>`, so the site never looks broken with photos absent.

## Outstanding

- `riscv-processor.jpg` and `fma-unit.jpg` are the last two placeholders. Both
  are RTL projects with no hardware to photograph; waveforms or a datapath
  diagram would do.
- A 21-second video of the ocean robot underway exists in the source material
  and is not used. The layout expects stills; swapping that card's `<img>` for a
  muted autoplaying `<video>` loop is a real option if the weight is acceptable.
