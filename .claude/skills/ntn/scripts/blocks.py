#!/usr/bin/env python3
"""blocks.py <page_id>: list a page's top-level blocks as `<block_id> <type> | <heading it falls under>`.
Blocks before the first heading are under "(top)". Pipe into grep/cut to pick block IDs."""
import json, subprocess, sys

def kids(i):
    out, cur = [], None
    while True:
        u = f"v1/blocks/{i}/children?page_size=100" + (f"&start_cursor={cur}" if cur else "")
        r = subprocess.run(["ntn", "api", u], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120)
        if r.returncode:
            sys.exit("ERR " + r.stderr[:300])
        d = json.loads(r.stdout)
        out += d["results"]
        if not d.get("has_more"):
            return out
        cur = d["next_cursor"]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    h = "(top)"
    for b in kids(sys.argv[1]):
        t = b["type"]
        if t.startswith("heading_"):
            h = "".join(x["plain_text"] for x in b[t]["rich_text"])
        print(b["id"], t, "|", h)
