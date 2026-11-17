#!/usr/bin/env python3
"""merge_blocks.py <src_page> '<heading regex>' <target_page> [--out-dir DIR] [--dry-run]
Appends the top-level blocks that fall under matching headings in src (the headings included,
nested children copied too) to the end of target. Use it to move a section between pages, or to
append new content: write it to a scratch page with `ntn pages create`, then merge from there.
Images cannot be copied through the API: a Notion-hosted image is downloaded to DIR/imgN.png and
replaced by an IMGPLACEHOLDERn paragraph, and an image with an empty URL (what `ntn pages create`
makes of `![caption](X)`) also becomes a placeholder. Upload each file with the Notion MCP
(notion-create-file-upload + curl -F file=@imgN.png), then replace the placeholder via
notion-update-page update_content with `<image source="file-upload://ID"></image>`
(escape underscores in old_str as \\_ if the placeholder text has any).
Child pages and databases under a matching heading are skipped. The source blocks are not deleted; delete them by ID afterwards (blocks.py lists them)."""
import json, os, re, subprocess, sys, urllib.request

def run(a):
    r = subprocess.run(["ntn", *a], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=180)
    if r.returncode:
        sys.exit("ERR " + " ".join(a[:3]) + " " + r.stderr[:400])
    return r.stdout

def api(*a):
    o = run(["api", *a])
    return json.loads(o) if o.strip() else {}

def kids(i):
    out, cur = [], None
    while True:
        d = api(f"v1/blocks/{i}/children?page_size=100" + (f"&start_cursor={cur}" if cur else ""))
        out += d["results"]
        if not d.get("has_more"):
            return out
        cur = d["next_cursor"]

IMGS = []

def clean_rt(rt):
    o = []
    for x in rt:
        if x["type"] == "text":
            o.append({"type": "text", "text": x["text"], "annotations": x["annotations"]})
        elif x["type"] == "equation":
            o.append({"type": "equation", "equation": x["equation"], "annotations": x["annotations"]})
        else:  # mentions: keep their text
            o.append({"type": "text", "text": {"content": x["plain_text"]}, "annotations": x["annotations"]})
    return o

def placeholder(note):
    k = len(IMGS)
    IMGS.append(note)
    return {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": f"IMGPLACEHOLDER{k}"}}]}}

def conv(b, out_dir, dry):
    t, v = b["type"], b[b["type"]]
    if t in ("image", "file"):
        if v["type"] == "external" and v["external"].get("url"):
            nb = {"type": "external", "external": v["external"]}
            if v.get("caption"):
                nb["caption"] = clean_rt(v["caption"])
            return {"type": t, t: nb}
        if v["type"] == "external":
            return placeholder("(empty URL: upload the figure by hand)")
        fn = os.path.join(out_dir, f"img{len(IMGS)}.png")
        if not dry:
            open(fn, "wb").write(urllib.request.urlopen(v["file"]["url"], timeout=60).read())
        return placeholder(fn)
    # color and list_format come back on reads but are rejected on writes
    nv = {k: val for k, val in v.items() if k not in ("color", "list_format") and val is not None}
    if "rich_text" in nv:
        nv["rich_text"] = clean_rt(nv["rich_text"])
    if t == "table_row":
        nv["cells"] = [clean_rt(c) for c in v["cells"]]
    if b.get("has_children") and t not in ("child_page", "child_database"):
        nv["children"] = [conv(c, out_dir, dry) for c in kids(b["id"])]
    return {"type": t, t: nv}

if __name__ == "__main__":
    argv, out_dir, dry = sys.argv[1:], ".", "--dry-run" in sys.argv
    argv = [a for a in argv if a != "--dry-run"]
    if "--out-dir" in argv:
        k = argv.index("--out-dir"); out_dir = argv[k + 1]; del argv[k:k + 2]
    if len(argv) != 3:
        sys.exit(__doc__)
    src, pat, tgt = argv[0], re.compile(argv[1]), argv[2]
    h, sel = None, []
    for b in kids(src):
        t = b["type"]
        if t.startswith("heading_"):
            h = "".join(x["plain_text"] for x in b[t]["rich_text"])
        if h and pat.search(h):
            if t in ("child_page", "child_database"):
                print("skipped", t, b["id"], "(pages cannot be copied; move them instead)")
            else:
                sel.append(b)
    new = [conv(b, out_dir, dry) for b in sel]
    if not dry:
        for i in range(0, len(new), 50):  # the API takes at most 100 children per call
            api(f"v1/blocks/{tgt}/children", "-X", "PATCH", "-d", json.dumps({"children": new[i:i + 50]}))
    print(("would append " if dry else "appended ") + str(len(new)), "blocks:", ", ".join(sorted({b["type"] for b in sel})))
    for k, f in enumerate(IMGS):
        print(f"IMGPLACEHOLDER{k} -> {f}")
