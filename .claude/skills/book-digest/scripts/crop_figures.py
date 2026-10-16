# /// script
# dependencies = ["pymupdf"]
# ///
"""Render each raster figure on a range of PDF pages as it appears in the book: its
frame (when the book draws one), a small white margin, and the caption below when it
is at most MAX_CAPTION_LINES long. The margin never reaches into surrounding text.

Usage: uv run crop_figures.py <book.pdf> <images-dir> <first-page> <last-page>
Pages are 1-based PDF page numbers. Writes <images-dir>/fig-<chapter>-<n>.png for
captioned figures (fig-p<page>-<i>.png otherwise) and prints one line per figure.
Vector-drawn diagrams have no raster image and are not found; crop those by hand.
"""
import re
import sys

import pymupdf

MARGIN = 8             # points of white space around frame + caption
MIN_SIZE = 60          # frame rules shorter than this (points) are ignored
MIN_FIGURE = 80        # images whose longer side is below this (points) are icons, not figures
MAX_CAPTION_LINES = 2  # longer captions stay out of the image
CAPTION_GAP = 30       # a caption must start within this many points below the frame
FRAME_GAP = 15         # frame rules sit within this many points of the image
DPI = 200
CAPTION = re.compile(r"(?:Figure|Fig\.)\s*(\d+)[.-](\d+)")


def frame_for(image, rules):
    """Frames are often drawn as separate lines: take the horizontal rules just above
    and below the image that span its width. Fall back to the image itself."""
    spans = [r for r in rules if r.x0 <= image.x0 + 2 and r.x1 >= image.x1 - 2]
    above = [r for r in spans if 0 <= image.y0 - r.y1 <= FRAME_GAP]
    below = [r for r in spans if 0 <= r.y0 - image.y1 <= FRAME_GAP]
    if not (above and below):
        return pymupdf.Rect(image)
    top, bottom = max(above, key=lambda r: r.y1), min(below, key=lambda r: r.y0)
    # the rules have zero height, so build the rect from coordinates (| skips empty rects)
    return pymupdf.Rect(min(top.x0, bottom.x0), top.y0, max(top.x1, bottom.x1), bottom.y1)


def caption_for(blocks, frame):
    for rect, text in blocks:
        if CAPTION.match(text) and 0 <= rect.y0 - frame.y1 <= CAPTION_GAP:
            return rect, text
    return None, None


def clip_for(page, blocks, frame, cap_rect):
    clip = pymupdf.Rect(frame)
    if cap_rect and len(page.get_textbox(cap_rect).splitlines()) <= MAX_CAPTION_LINES:
        clip |= cap_rect
    clip = (clip + (-MARGIN, -MARGIN, MARGIN, MARGIN)) & page.rect
    for rect, _ in blocks:  # keep the margin clear of body text above and below
        if rect.x1 > clip.x0 and rect.x0 < clip.x1:
            if rect.y1 <= frame.y0:
                clip.y0 = max(clip.y0, rect.y1 + 1)
            elif clip.y1 - MARGIN <= rect.y0 < clip.y1:
                clip.y1 = rect.y0 - 1
    return clip


def main(pdf, outdir, first, last):
    doc = pymupdf.open(pdf)
    for pno in range(first - 1, last):
        page = doc[pno]
        rules = [d["rect"] for d in page.get_drawings() if d["rect"].width > MIN_SIZE and d["rect"].height < 1]
        blocks = [(pymupdf.Rect(b[:4]), b[4]) for b in page.get_text("blocks")]
        images = [pymupdf.Rect(i["bbox"]) for i in page.get_image_info()]
        figures = sorted((r for r in images if max(r.width, r.height) >= MIN_FIGURE), key=lambda r: r.y0)
        for i, image in enumerate(figures):
            frame = frame_for(image, rules)
            cap_rect, text = caption_for(blocks, frame)
            match = CAPTION.match(text) if text else None
            name = f"fig-{match[1]}-{match[2]}.png" if match else f"fig-p{pno + 1}-{i}.png"
            page.get_pixmap(clip=clip_for(page, blocks, frame, cap_rect), dpi=DPI).save(f"{outdir}/{name}")
            notes = [n for n, missing in (("no frame", frame == image), ("no caption", not match)) if missing]
            print(f"p{pno + 1} -> {name}" + (f"  ({', '.join(notes)})" if notes else ""))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
