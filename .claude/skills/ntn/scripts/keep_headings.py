#!/usr/bin/env python3
"""keep_headings.py <page_id> '<regex of heading names to KEEP>' [--dry-run]
Deletes every top-level block whose enclosing heading does not match the regex (used to split a
duplicated page into parts). '\\(top\\)' keeps the blocks before the first heading. Include H3
names under a kept H2 in the regex: each block counts as under its nearest heading of any level.
Deleting a toggle deletes its nested content; deleting a heading does not delete what follows it."""
import json, re, subprocess, sys

def ntn(*a):
    return subprocess.run(["ntn", *a], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120)

def kids(i):
    out, cur = [], None
    while True:
        r = ntn("api", f"v1/blocks/{i}/children?page_size=100" + (f"&start_cursor={cur}" if cur else ""))
        if r.returncode:
            sys.exit("ERR " + r.stderr[:300])
        d = json.loads(r.stdout)
        out += d["results"]
        if not d.get("has_more"):
            return out
        cur = d["next_cursor"]

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry = "--dry-run" in sys.argv
    if len(args) != 2:
        sys.exit(__doc__)
    page, rx = args[0], re.compile(args[1])
    h, kept, gone = "(top)", [], 0
    for b in kids(page):
        t = b["type"]
        if t.startswith("heading_"):
            h = "".join(x["plain_text"] for x in b[t]["rich_text"])
        if rx.search(h):
            if t.startswith("heading_"):
                kept.append(h)
            continue
        gone += 1
        if dry:
            print("would delete", b["id"], t, "|", h)
        elif ntn("api", f"v1/blocks/{b['id']}", "-X", "DELETE").returncode:
            print("FAIL", b["id"])
    print(("would delete " if dry else "deleted ") + str(gone) + " blocks; headings kept:", kept)
