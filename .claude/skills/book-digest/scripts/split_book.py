#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf"]
# ///
"""Split an EPUB or PDF into one markdown/text file per chapter.

EPUB: split by the table of contents (stdlib only).
PDF:  split by the PDF outline if PyMuPDF is installed; otherwise dump
      pages to _pages.txt and split by --ranges "N:Title:start-end,...".
Images go to <outdir>/../images/ and are referenced in the chapter text as
![alt](../images/name.png) at the place they appear (EPUB) or at the end of
their page (PDF).
"""
import argparse
import html
import posixpath
import re
import subprocess
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "untitled"


def write_chapter(outdir, num, title, body):
    path = outdir / f"{num:02d}-{slug(title)}.md"
    path.write_text(f"# {title}\n\n{body.strip()}\n", encoding="utf-8")
    print(f"{path.name}: {len(body.split())} words")


# ---------- EPUB ----------

class HtmlToText(HTMLParser):
    BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "blockquote"}

    def __init__(self, on_image=None):
        super().__init__()
        self.out, self.in_pre, self.skip = [], 0, 0
        self.on_image = on_image

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        src = attrs.get("src") or attrs.get("xlink:href") or attrs.get("href")
        if tag in ("img", "image") and src and self.on_image:
            name = self.on_image(src)
            if name:
                self.out.append(f"\n\n![{attrs.get('alt', '')}](../images/{name})\n\n")
        elif tag in ("script", "style"):
            self.skip += 1
        elif tag == "pre":
            self.in_pre += 1
            self.out.append("\n```\n")
        elif tag in ("h1", "h2", "h3", "h4"):
            self.out.append("\n\n" + "#" * (int(tag[1]) + 1) + " ")
        elif tag == "li":
            self.out.append("\n- ")
        elif tag in self.BLOCK:
            self.out.append("\n\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        elif tag == "pre":
            self.in_pre -= 1
            self.out.append("\n```\n")
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self.skip:
            return
        self.out.append(data if self.in_pre else re.sub(r"\s+", " ", data))

    def text(self):
        return re.sub(r"\n{3,}", "\n\n", "".join(self.out))


def html_to_text(markup, on_image=None):
    parser = HtmlToText(on_image)
    parser.feed(markup)
    return parser.text()


def local(tag):
    return tag.rsplit("}", 1)[-1]


def epub_toc(z, opf_path, opf):
    """Return [(title, href_without_fragment)] from nav.xhtml or toc.ncx."""
    base = posixpath.dirname(opf_path)
    items = {i.get("id"): i for i in opf.iter() if local(i.tag) == "item"}
    nav = next((i for i in items.values() if "nav" in (i.get("properties") or "").split()), None)
    entries = []
    if nav is not None:
        nav_path = posixpath.join(base, nav.get("href"))
        root = ET.fromstring(z.read(nav_path))
        toc = next((n for n in root.iter() if local(n.tag) == "nav"
                    and "toc" in " ".join(v for k, v in n.attrib.items() if k.endswith("type"))), None)
        if toc is not None:
            ol = next((c for c in toc if local(c.tag) == "ol"), None)
            for li in (ol if ol is not None else []):
                a = next((n for n in li.iter() if local(n.tag) == "a"), None)
                if a is not None and a.get("href"):
                    href = posixpath.normpath(posixpath.join(posixpath.dirname(nav_path), a.get("href")))
                    entries.append(("".join(a.itertext()).strip(), href))
    if not entries:
        ncx = next((i for i in items.values() if i.get("media-type") == "application/x-dtbncx+xml"), None)
        if ncx is not None:
            ncx_path = posixpath.join(base, ncx.get("href"))
            root = ET.fromstring(z.read(ncx_path))
            navmap = next(n for n in root.iter() if local(n.tag) == "navMap")
            for point in (c for c in navmap if local(c.tag) == "navPoint"):
                label = "".join(next(n for n in point.iter() if local(n.tag) == "text").itertext())
                src = next(n for n in point.iter() if local(n.tag) == "content").get("src")
                entries.append((label.strip(), posixpath.normpath(posixpath.join(posixpath.dirname(ncx_path), src))))
    return [(t, h.split("#")[0]) for t, h in entries]


def split_epub(book, outdir):
    z = zipfile.ZipFile(book)
    container = ET.fromstring(z.read("META-INF/container.xml"))
    opf_path = next(n for n in container.iter() if local(n.tag) == "rootfile").get("full-path")
    opf = ET.fromstring(z.read(opf_path))
    base = posixpath.dirname(opf_path)
    items = {i.get("id"): posixpath.normpath(posixpath.join(base, i.get("href")))
             for i in opf.iter() if local(i.tag) == "item"}
    spine = [items[r.get("idref")] for r in opf.iter() if local(r.tag) == "itemref"]

    toc = epub_toc(z, opf_path, opf)
    starts = {}
    for title, href in toc:
        if href in spine and spine.index(href) not in starts:
            starts[spine.index(href)] = title
    if not starts:
        sys.exit("No usable table of contents; falling back is not implemented. Inspect the EPUB manually.")

    order = sorted(starts)
    if order[0] != 0:
        order.insert(0, 0)
        starts[0] = "Front matter"
    images = outdir.parent / "images"
    images.mkdir(exist_ok=True)

    def extractor(doc_path):
        def extract(src):
            member = posixpath.normpath(posixpath.join(posixpath.dirname(doc_path), src.split("#")[0]))
            if member not in z.namelist():
                return None
            name = member.replace("/", "_")
            (images / name).write_bytes(z.read(member))
            return name
        return extract

    for n, (a, b) in enumerate(zip(order, order[1:] + [len(spine)])):
        body = "\n\n".join(html_to_text(z.read(p).decode("utf-8", "replace"), extractor(p))
                           for p in spine[a:b])
        write_chapter(outdir, n, html.unescape(starts[a]), body)


# ---------- PDF ----------

def pdf_pages(book):
    text = subprocess.run(["pdftotext", "-layout", str(book), "-"],
                          check=True, capture_output=True, text=True).stdout
    return text.split("\f")


MIN_IMAGE_PX = 80  # skip icons, bullets and rules


def pdf_images(book, images):
    """Return {page_number: [image file names]}.

    With PyMuPDF: renders each image's area on the page at 2x (a screenshot,
    so masks and overlaid labels come out right). Without it: pdfimages.
    Vector-only diagrams are not detected; see SKILL.md for the fallback.
    """
    images.mkdir(exist_ok=True)
    found = {}
    try:
        import pymupdf as fitz
    except ImportError:
        subprocess.run(["pdfimages", "-png", "-p", str(book), str(images / "p")], check=True)
        for f in sorted(images.glob("p-*.png")):
            page = int(f.name.split("-")[1])
            found.setdefault(page, []).append(f.name)
        return found
    doc = fitz.open(book)
    for page in doc:
        for k, rect in enumerate(r for img in page.get_images(full=True) for r in page.get_image_rects(img[0])):
            rect = rect & page.rect
            if rect.is_empty or min(rect.width, rect.height) < MIN_IMAGE_PX / 2:
                continue
            name = f"p{page.number + 1:04d}-{k}.png"
            page.get_pixmap(clip=rect, dpi=144).save(images / name)
            found.setdefault(page.number + 1, []).append(name)
    return found


def split_pdf(book, outdir, ranges):
    pages = pdf_pages(book)
    figures = pdf_images(book, outdir.parent / "images")

    def page_text(p):
        refs = "".join(f"\n![page {p}](../images/{name})\n" for name in figures.get(p, []))
        return f"=== PAGE {p} ===\n{pages[p - 1]}{refs}"

    if ranges:
        for part in ranges.split(","):
            num, rest = part.split(":", 1)
            title, span = rest.rsplit(":", 1)
            start, end = map(int, span.split("-"))
            write_chapter(outdir, int(num), title, "\n".join(page_text(p) for p in range(start, end + 1)))
        return

    try:
        import pymupdf as fitz
        outline = [(t, p) for lvl, t, p in fitz.open(book).get_toc() if lvl == 1 and p > 0]
    except ImportError:
        outline = []
    if outline:
        bounds = [p for _, p in outline[1:]] + [len(pages) + 1]
        for n, ((title, start), end) in enumerate(zip(outline, bounds), 1):
            write_chapter(outdir, n, title, "\n".join(
                page_text(p) for p in range(start, min(end, len(pages) + 1))))
        return

    dump = outdir / "_pages.txt"
    dump.write_text("".join(page_text(p) for p in range(1, len(pages) + 1)), encoding="utf-8")
    print(f"No PDF outline found (or PyMuPDF missing). Wrote {dump}; rerun with --ranges.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book", type=Path)
    ap.add_argument("outdir", type=Path)
    ap.add_argument("--ranges", help='PDF only: "1:Title:15-48,2:Title:49-80" (PDF page numbers)')
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    suffix = args.book.suffix.lower()
    if suffix == ".epub":
        split_epub(args.book, args.outdir)
    elif suffix == ".pdf":
        split_pdf(args.book, args.outdir, args.ranges)
    else:
        sys.exit("Unsupported format: use .epub or .pdf")


if __name__ == "__main__":
    main()
