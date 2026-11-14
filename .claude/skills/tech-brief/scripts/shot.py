# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright>=1.45"]
# ///
"""Screenshot figures from a web page.

  shot.py <url> <outdir> --list                      list candidate figures (index, size, alt, selector)
  shot.py <url> <outdir> --pick 0,3 --name oidc      screenshot those candidates -> <name>-<i>.png
  shot.py <url> <outdir> --selector "figure#x" --name n   screenshot one element

Candidates are <img>, <svg>, <figure>, <canvas> and <pre class*=mermaid> at least
200x120 CSS px. Element screenshots include the rendered caption when the
element is a <figure>. Scale is 2x for legibility.
"""
import argparse, json, pathlib, subprocess, sys
from playwright.sync_api import sync_playwright, Error

JS = """() => {
  const out = [];
  const els = document.querySelectorAll('figure, img, svg, canvas, pre.mermaid, div.mermaid');
  els.forEach((e) => {
    if (e.closest('figure') && e.tagName !== 'FIGURE') return;   // figure wins over its child
    if (e.tagName === 'svg' && e.closest('svg') !== e) return;
    const r = e.getBoundingClientRect();
    if (r.width < 200 || r.height < 120) return;
    const i = out.length;
    e.setAttribute('data-shot', i);
    const cap = e.querySelector && e.querySelector('figcaption');
    out.push({i, tag: e.tagName.toLowerCase(), w: Math.round(r.width), h: Math.round(r.height),
              alt: (e.getAttribute('alt') || (cap && cap.innerText) || e.getAttribute('aria-label') || '').slice(0, 120),
              src: e.currentSrc || e.getAttribute('src') || ''});
  });
  return out;
}"""

def open_page(p, url):
    try:
        b = p.chromium.launch()
    except Error:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1400, "height": 1000}, device_scale_factor=2)
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")  # trigger lazy images
    page.wait_for_timeout(1500)
    page.evaluate("window.scrollTo(0, 0)")
    return b, page

HIDE_OVERLAYS = """() => document.querySelectorAll('body *').forEach(e => {
  const p = getComputedStyle(e).position;
  if ((p === 'fixed' || p === 'sticky') && !e.querySelector('[data-shot]') && !e.closest('[data-shot]')) e.style.setProperty('display', 'none', 'important');
  document.documentElement.style.overflow = 'auto'; document.body.style.overflow = 'auto';
})"""

def snap(page, loc, f):
    page.evaluate(HIDE_OVERLAYS)  # cookie banners, sticky headers, modals
    loc.scroll_into_view_if_needed()
    loc.evaluate("""async (e) => {
      const imgs = e.tagName === 'IMG' ? [e] : [...e.querySelectorAll('img')];
      imgs.forEach(i => i.loading = 'eager');
      await Promise.all(imgs.map(i => i.complete && i.naturalWidth ? 0 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 8000); })));
    }""")
    page.wait_for_timeout(500)
    loc.screenshot(path=str(f)); print(f)

def main():
    a = argparse.ArgumentParser()
    a.add_argument("url"); a.add_argument("outdir")
    a.add_argument("--list", action="store_true")
    a.add_argument("--pick"); a.add_argument("--selector"); a.add_argument("--name", default="fig")
    o = a.parse_args()
    out = pathlib.Path(o.outdir); out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b, page = open_page(p, o.url)
        cands = page.evaluate(JS)
        if o.list or not (o.pick or o.selector):
            for c in cands:
                print(json.dumps(c))
        elif o.selector:
            f = out / f"{o.name}.png"
            snap(page, page.locator(o.selector).first, f)
        else:
            for i in [int(x) for x in o.pick.split(",")]:
                f = out / f"{o.name}-{i}.png"
                snap(page, page.locator(f'[data-shot="{i}"]'), f)
        b.close()

if __name__ == "__main__":
    main()
