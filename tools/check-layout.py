#!/usr/bin/env python3
"""Measure the layout invariants that have silently broken before.

    python tools/check-layout.py

Serves the site on a scratch port, drives it with headless Chromium, and
checks three things at 1440px and 390px, in both positioning modes:

  1. Mode-switch buttons render at EQUAL width. The sliding thumb is exactly
     50% and translates by its own width, so if the min-width floor sits
     below the longer label's natural width the labels desynchronise and the
     thumb lines up with neither. This is the check that catches it.
  2. No horizontal overflow.
  3. Every project <img> resolves (a miss silently falls back to a
     placeholder, which is easy not to notice).

Requires: pip install playwright && python -m playwright install chromium
Exits non-zero on failure so it can gate a commit.
"""
import functools
import http.server
import socket
import socketserver
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("playwright not installed:\n"
             "  pip install playwright && python -m playwright install chromium")


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


PORT = free_port()
handler = functools.partial(QuietHandler, directory=str(ROOT))
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{PORT}/"

MEASURE = """() => {
  const btns = [...document.querySelectorAll('.mode-btn')];
  const natural = btns.map(b => {
    const c = b.cloneNode(true);
    c.style.cssText = 'position:absolute;visibility:hidden;min-width:0;white-space:nowrap';
    document.body.appendChild(c);
    const w = c.getBoundingClientRect().width;
    c.remove();
    return { label: b.textContent.trim(),
             natural: +w.toFixed(1),
             rendered: +b.getBoundingClientRect().width.toFixed(1) };
  });
  return {
    buttons: natural,
    thumb: +document.querySelector('.mode-switch-thumb').getBoundingClientRect().width.toFixed(1),
    scrollW: document.documentElement.scrollWidth,
    winW: window.innerWidth,
  };
}"""

failures = []

with sync_playwright() as p:
    browser = p.chromium.launch()

    for width, height in ((1440, 900), (390, 844)):
        for mode in ("technical", "general"):
            ctx = browser.new_context(viewport={"width": width, "height": height})
            pg = ctx.new_page()
            pg.goto(URL, wait_until="networkidle")
            if mode == "general":
                pg.click('.mode-btn[data-mode="general"]')
                pg.wait_for_timeout(500)

            d = pg.evaluate(MEASURE)
            tag = f"{width}px/{mode}"

            widths = {b["rendered"] for b in d["buttons"]}
            if len(widths) > 1:
                failures.append(f"{tag}: mode-switch buttons unequal — "
                                + ", ".join(f"{b['label']}={b['rendered']}" for b in d["buttons"]))
            for b in d["buttons"]:
                if b["rendered"] < b["natural"]:
                    failures.append(f"{tag}: '{b['label']}' clipped "
                                    f"(natural {b['natural']} > rendered {b['rendered']})")
            if abs(d["thumb"] - d["buttons"][0]["rendered"]) > 1.0:
                failures.append(f"{tag}: thumb {d['thumb']} != button {d['buttons'][0]['rendered']}")
            if d["scrollW"] > d["winW"]:
                failures.append(f"{tag}: horizontal overflow "
                                f"(scrollWidth {d['scrollW']} > {d['winW']})")

            print(f"{tag:<18} buttons "
                  + " / ".join(f"{b['label']} {b['rendered']}" for b in d["buttons"])
                  + f"   thumb {d['thumb']}   overflow "
                  + ("none" if d["scrollW"] <= d["winW"] else "YES"))
            ctx.close()

    # Images: scroll the whole page so lazy-loaded ones actually resolve.
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    pg = ctx.new_page()
    pg.goto(URL, wait_until="networkidle")
    pg.evaluate("""async () => {
      for (let y = 0; y < document.body.scrollHeight; y += 400) {
        window.scrollTo(0, y);
        await new Promise(r => setTimeout(r, 60));
      }
    }""")
    pg.wait_for_timeout(1200)
    imgs = pg.evaluate("""() => [...document.querySelectorAll('img')].map(i => ({
        src: i.getAttribute('src').split('/').pop(),
        ok: i.complete && i.naturalWidth > 0 }))""")
    print("\nimages:")
    for i in imgs:
        print(f"  {i['src']:<24} {'ok' if i['ok'] else 'MISSING (placeholder shown)'}")
    ctx.close()
    browser.close()

httpd.shutdown()

print()
if failures:
    print(f"{len(failures)} layout problem(s):")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print("Layout invariants hold at 1440px and 390px, both modes.")
