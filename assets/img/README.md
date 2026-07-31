# Project images

Photos are referenced by the **exact filenames** below. Until a file exists the
site shows a styled placeholder in its place — nothing looks broken, so the
remaining ones can be added one at a time.

## In place

| Filename | Where it appears | What it shows |
|---|---|---|
| `logger-fleet.jpg` | Vehicle telemetry logger card | A finished unit in its 3D-printed enclosure, labelled `OLTO VCU LOGGER / UNIT 04` |
| `logger-bench.jpg` | About section | A Teensy 4.1 stacked on the CAN transceiver board, held up mid-build |
| `xdemics-robot.jpg` | Bioreactor automation card | The fixturing and vibration rig on the bench, orange printed clamps holding the bioreactor |
| `baseball-loader.jpg` | Pitching machine loader card | The built ramp on its weighted stand, feeding the machine |
| `led-zeppelin.jpg` | Audio visualizer card | The bench setup — breadboard, LED bar, speakers, STM32 and FPGA boards on ribbon cable |
| `ocean-robot.jpg` | Ocean surface robot card | The robot floating in shallow water, anemometer above the PVC and foam frame |
| `simon-game.jpg` | Simon game card | The breadboard close up: two tactile buttons wired to red and green LEDs |

## Still missing

| Filename | Project | Good shot to use |
|---|---|---|
| `riscv-processor.jpg` | RISC-V multicycle processor | Simulation waveforms, or a block diagram of the datapath |
| `fma-unit.jpg` | Floating-point multiply-accumulate unit | Block diagram, or synthesis/timing results |

Both are RTL projects with no physical hardware, so a clean screenshot of
waveforms in Questa — or a hand-drawn datapath — beats nothing. Until then
their cards show a numbered placeholder.

## Guidelines

- **Format:** `.jpg` for photos. If you only have `.png`, either rename it to
  `.jpg` (browsers read the real format, not the extension) or update the `src`
  in `index.html`.
- **Size:** roughly 1600×1067 (3:2). The cards use `object-fit: cover` at a 3:2
  aspect, so anything close to that crops predictably.
- **Weight:** keep each file under ~400 KB so the page stays fast. The current
  set runs 122–366 KB.
- **Framing:** images are cropped to fill, so leave a little breathing room
  around the subject — edges may be trimmed.
- **Bench photos beat renders.** A slightly messy real photo of hardware on a
  desk is more convincing to a hiring engineer than a clean CAD render. Every
  photo currently on the site is a real one.

After adding a file, run `python tools/check-layout.py` — it reports which
images resolve and which are still falling back to placeholders.
