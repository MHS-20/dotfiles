"""Insert a local PNG into an existing Notion page after the first block whose text contains <anchor>.

  python3 insert_image.py <page-id> "<anchor text>" <image.png> "<caption>"
"""
import json, subprocess, sys
from pathlib import Path

def ntn(*args):
    r = subprocess.run(["ntn", *args], stdin=subprocess.DEVNULL, capture_output=True, timeout=120)
    if r.returncode:
        sys.exit(f"ntn {args[:2]} failed: {r.stderr.decode()}")
    return r.stdout.decode()

page, anchor, path, cap = sys.argv[1], sys.argv[2], Path(sys.argv[3]), sys.argv[4]
blocks, cursor = [], None
while True:
    r = json.loads(ntn("api", f"v1/blocks/{page}/children?page_size=100" + (f"&start_cursor={cursor}" if cursor else "")))
    blocks += r["results"]
    if not r.get("has_more"): break
    cursor = r["next_cursor"]
target = next((b for b in blocks if anchor in "".join(t["plain_text"] for t in b.get(b["type"], {}).get("rich_text", []))), None)
if not target:
    sys.exit(f"anchor not found: {anchor}")
up = json.loads(ntn("api", "v1/file_uploads", "-X", "POST", "-d", json.dumps(
    {"mode": "single_part", "filename": path.name, "content_type": "image/png"})))
ntn("api", f"v1/file_uploads/{up['id']}/send", "-X", "POST", "--file", str(path))
child = {"type": "image", "image": {"type": "file_upload", "file_upload": {"id": up["id"]},
         "caption": [{"type": "text", "text": {"content": cap[:2000]}}]}}
ntn("api", f"v1/blocks/{page}/children", "-X", "PATCH", "-d", json.dumps(
    {"children": [child], "position": {"type": "after_block", "after_block": {"id": target["id"]}}}))
print("inserted after", target["id"])
