#!/usr/bin/env python3
"""replace_text.py <page_id> '<json list of [old, new]>' [--regex] [--top-only] [--dry-run]
Find-and-replace inside a page's blocks through the API, keeping inline formatting (bold, code,
links) of the text around each edit. Walks nested blocks and table cells; skips child pages.
Use it where notion-update-page update_content fails to match (inline code, escaped quotes).
--regex treats each `old` as a Python regex (new may use \\1); --top-only skips nested blocks.
Examples:
  replace_text.py <id> '[["Lesson 12","F8"],["stage 1 ",""]]'
  replace_text.py <id> '[["\\\\b(ing_|ING_)",""]]' --regex      # strip a prefix at word starts
Mentions and equations inside an edited block are kept as plain text spans."""
import json, re, subprocess, sys

def api(*a):
    r = subprocess.run(["ntn", "api", *a], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120)
    if r.returncode:
        print("ERR", r.stderr[:300])
        return {}
    return json.loads(r.stdout) if r.stdout.strip() else {}

def kids(i):
    out, cur = [], None
    while True:
        d = api(f"v1/blocks/{i}/children?page_size=100" + (f"&start_cursor={cur}" if cur else ""))
        out += d.get("results", [])
        if not d.get("has_more"):
            return out
        cur = d["next_cursor"]

def edit(rt, reps, use_rx, hits):
    """Apply replacements to one rich_text array. Returns the new array, or None if unchanged."""
    text = "".join(x["plain_text"] for x in rt)
    owner = [i for i, x in enumerate(rt) for _ in x["plain_text"]]  # span that owns each char
    changed = False
    for k, (old, new) in enumerate(reps):
        rx = re.compile(old if use_rx else re.escape(old))
        for m in reversed(list(rx.finditer(text))):
            a, b = m.span()
            rep = m.expand(new) if use_rx else new
            if (a, b) == (a, a) and not rep:
                continue
            src = owner[a] if a < len(owner) else (owner[-1] if owner else 0)
            text = text[:a] + rep + text[b:]
            owner = owner[:a] + [src] * len(rep) + owner[b:]
            hits[k] += 1
            changed = True
    if not changed:
        return None
    segs = []
    for ch, ow in zip(text, owner):
        if segs and segs[-1][0] == ow:
            segs[-1][1] += ch
        else:
            segs.append([ow, ch])
    out = []
    for ow, s in segs:
        x = rt[ow]
        link = (x.get("text") or {}).get("link") if x["type"] == "text" else None
        out.append({"type": "text", "text": {"content": s, "link": link}, "annotations": x["annotations"]})
    return out

def walk(i, reps, use_rx, nested, dry, hits):
    n = 0
    for b in kids(i):
        t, v = b["type"], b.get(b["type"], {})
        body = None
        if t == "table_row":
            cells = [edit(c, reps, use_rx, hits) for c in v["cells"]]
            if any(c is not None for c in cells):
                body = {t: {"cells": [c if c is not None else old for c, old in zip(cells, v["cells"])]}}
        elif isinstance(v, dict) and v.get("rich_text") is not None:
            new = edit(v["rich_text"], reps, use_rx, hits)
            if new is not None:
                body = {t: {"rich_text": new}}
                if t == "code":
                    body[t]["language"] = v["language"]
        if body:
            n += 1
            if dry:
                print("would change", b["id"], t)
            else:
                api(f"v1/blocks/{b['id']}", "-X", "PATCH", "-d", json.dumps(body))
        if nested and b.get("has_children") and t not in ("child_page", "child_database"):
            n += walk(b["id"], reps, use_rx, nested, dry, hits)
    return n

if __name__ == "__main__":
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    reps = json.loads(args[1])
    hits = [0] * len(reps)
    n = walk(args[0], reps, "--regex" in flags, "--top-only" not in flags, "--dry-run" in flags, hits)
    for (old, _), h in zip(reps, hits):
        print(("MISS " if h == 0 else f"{h:>4} ") + old[:70])
    print(n, "blocks", "would change" if "--dry-run" in flags else "changed")
