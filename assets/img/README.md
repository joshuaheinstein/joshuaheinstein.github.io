# Project images

Drop photos in this folder using the **exact filenames** below and they appear on
the site automatically. Until a file exists, the site shows a styled placeholder
in its place — nothing looks broken, so you can add them one at a time.

| Filename | Project | Good shot to use |
|---|---|---|
| `logger-fleet.jpg` | Vehicle telemetry loggers (Infinite Machine) | The twelve units laid out together, or one mounted in a vehicle |
| `led-zeppelin.jpg` | LED Zeppelin audio visualizer | The RGB display lit up mid-song, ideally in low light |
| `riscv-processor.jpg` | RISC-V multicycle processor | Simulation waveforms, or a block diagram of the datapath |
| `xdemics-robot.jpg` | Bioreactor automation robot | The assembled multi-axis machine |
| `fma-unit.jpg` | Floating-point multiply-accumulate unit | Block diagram, or synthesis/timing results |
| `ocean-robot.jpg` | Autonomous oceanic surface robot | The robot on the water |
| `simon-game.jpg` | Simon game on RISC-V MCU | The breadboard with LEDs lit |

### Extra shots used only by `deck.html`

The interview deck reuses the images above and adds two of its own. Same rules
apply — missing files fall back to a placeholder that names the shot to take.

| Filename | Where it appears | Good shot to use |
|---|---|---|
| `logger-app.jpg` | Deck slide 4 | Screenshot of the desktop app: live decode with a chart and the raw-frame pane visible, ideally on a real capture |
| `logger-install.jpg` | Deck slide 4 | One logger mounted in a vehicle with the harness run — shows the packaging constraint |

## Guidelines

- **Format:** `.jpg` for photos. If you only have `.png`, either rename it to
  `.jpg` (browsers read the real format, not the extension) or update the `src`
  in `index.html`.
- **Size:** roughly 1600×1000 px. Larger is wasted; smaller looks soft on
  retina screens.
- **Weight:** keep each file under ~400 KB so the page stays fast.
- **Framing:** images are cropped to fill (`object-fit: cover`), so leave a
  little breathing room around the subject — edges may be trimmed.
- **Bench photos beat renders.** A slightly messy real photo of hardware on a
  desk is more convincing to a hiring engineer than a clean CAD render.

## Video

The layout currently expects still images. If you have a clip worth showing
(the visualizer reacting to music is the obvious candidate), say so and the
media block can be swapped for a muted autoplaying `<video>` loop.
