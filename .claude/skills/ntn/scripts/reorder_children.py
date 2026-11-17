#!/usr/bin/env python3
"""reorder_children.py <parent_page_id> <spec_file> [--dry-run]
Puts a page's child pages in a given order under given headings. Notion's API cannot move a block
within a page, and `ntn pages edit` does not move child pages; a page moved with
`POST v1/pages/<id>/move` lands at the end of its new parent. So the script moves every child page
to a temporary page, deletes the parent's headings, then appends each heading and moves its pages
back in order. Child pages not named in the spec go back at the end, under no heading. The
temporary page is trashed at the end (restorable from Notion's trash).

Spec file: one heading line (`#`, `##` or `###` + text), then page IDs (32 hex, dashes allowed,
anything after the ID on the line is ignored), e.g. a TSV `code<TAB>id<TAB>title` reformatted:
    ### A. C Language
    4196da3fac8580deb396f422d103d5c6  A1 Output parameters
    ...
The parent may hold only child pages, headings and empty paragraphs; anything else aborts the run
so no text is lost. Takes about 1-2 s per page."""
import json, re, subprocess, sys

def ntn(*a):
    r = subprocess.run(["ntn", *a], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=180)
    if r.returncode:
        sys.exit("ERR " + " ".join(a[:3]) + " " + r.stderr[:300])
    return json.loads(r.stdout) if r.stdout.strip().startswith("{") else r.stdout

def kids(i):
    out, cur = [], None
    while True:
        d = ntn("api", f"v1/blocks/{i}/children?page_size=100" + (f"&start_cursor={cur}" if cur else ""))
        out += d["results"]
        if not d.get("has_more"):
            return out
        cur = d["next_cursor"]

def move(page, parent):
    ntn("api", f"v1/pages/{page}/move", "-X", "POST", "-d",
        json.dumps({"parent": {"type": "page_id", "page_id": parent}}))

def heading(level, text):
    t = f"heading_{level}"
    return {"type": t, t: {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def norm(i):
    return i.replace("-", "")

if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    if len(args) != 2:
        sys.exit(__doc__)
    parent = norm(args[0])
    sections, seen = [], set()
    for line in open(args[1]):
        line = line.strip()
        if m := re.match(r"(#{1,3})\s+(.+)", line):
            sections.append((len(m[1]), m[2], []))
        elif m := re.match(r"([0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12})", line):
            if not sections:
                sys.exit("spec: page ID before the first heading: " + line)
            i = norm(m[1])
            if i in seen:
                sys.exit("spec: page listed twice: " + i)
            seen.add(i)
            sections[-1][2].append(i)
    blocks = kids(parent)
    bad = [b for b in blocks if b["type"] not in ("child_page", "heading_1", "heading_2", "heading_3")
           and not (b["type"] == "paragraph" and not b["paragraph"]["rich_text"])]
    if bad:
        sys.exit("parent holds other content, aborting: " + ", ".join(f"{b['id']} {b['type']}" for b in bad[:10]))
    children = [norm(b["id"]) for b in blocks if b["type"] == "child_page"]
    missing = seen - set(children)
    if missing:
        sys.exit("spec names pages that are not children of the parent: " + ", ".join(sorted(missing)))
    rest = [c for c in children if c not in seen]
    print(f"{len(children)} child pages, {len(sections)} headings, {len(rest)} unlisted (go last)")
    if dry:
        for lvl, text, ids in sections:
            print("#" * lvl, text, len(ids))
        sys.exit(0)
    out = ntn("pages", "create", "--parent", f"page:{parent}", "--content=reorder temp", "--plain")
    tmp = norm(re.search(r"[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}", out)[0])
    print("temp page", tmp, "(if the run dies, the pages are there)", flush=True)
    for c in children:
        move(c, tmp)
    for b in kids(parent):
        if norm(b["id"]) != tmp:
            ntn("api", f"v1/blocks/{b['id']}", "-X", "DELETE")
    for lvl, text, ids in sections:
        ntn("api", f"v1/blocks/{parent}/children", "-X", "PATCH", "-d", json.dumps({"children": [heading(lvl, text)]}))
        for i in ids:
            move(i, parent)
        print(text, len(ids), flush=True)
    for i in rest:
        move(i, parent)
    ntn("api", f"v1/pages/{tmp}", "-X", "PATCH", "-d", '{"in_trash": true}')
    print("done; temp page trashed")
