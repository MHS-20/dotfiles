#!/usr/bin/env python3
"""wait_populated.py <page_id> [timeout_s=300]: wait until a page made by notion-duplicate-page is
readable (the API answers 'copy_indicator is not supported' while copying), then print its
top-level block count. Run one duplicate at a time: two concurrent duplicates of the same page
can leave one as an empty stub."""
import json, subprocess, sys, time

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    page, limit = sys.argv[1], float(sys.argv[2]) if len(sys.argv) == 3 else 300
    end = time.time() + limit
    while time.time() < end:
        r = subprocess.run(["ntn", "api", f"v1/blocks/{page}/children?page_size=100"],
                           stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120)
        if r.returncode == 0:
            d = json.loads(r.stdout)
            print(len(d["results"]), "blocks" + (" (first 100; more exist)" if d.get("has_more") else ""))
            sys.exit(0)
        time.sleep(5)
    sys.exit("TIMEOUT")
