"""Create a Notion page from markdown with local images, via ntn.

  python3 push.py <parent-page-id> <title> <guide.md>

Images (`![caption](path.png)`, PNG, at most 5 MB) are uploaded single-part via `ntn api`; each
image line is first written as a placeholder paragraph, then replaced in place
by an image block. Prints the new page id.
"""
import json, re, subprocess, sys
from pathlib import Path

def ntn(*args, stdin=None):
    r = subprocess.run(["ntn", *args], input=stdin, stdin=None if stdin is not None else subprocess.DEVNULL,
                       capture_output=True, timeout=120)
    if r.returncode:
        sys.exit(f"ntn {args[:2]} failed: {r.stderr.decode()}")
    return r.stdout.decode()

parent, title, md = sys.argv[1], sys.argv[2], Path(sys.argv[3])
IMG = re.compile(r"^!\[(.*?)\]\((.+?)\)\s*$")
images, lines = [], []
for line in md.read_text().splitlines():
    m = IMG.match(line)
    if m and not m[2].startswith("http"):
        lines.append(f"IMGSLOT{len(images)}")
        images.append((m[1], (md.parent / m[2]).resolve()))
    else:
        lines.append(line)

body = f"---\ntitle: {title}\n---\n" + "\n".join(lines)
page = ntn("pages", "create", f"--parent=page:{parent}", f"--content={body}", "--plain").split()[0]

blocks, cursor = [], None
while True:
    q = f"v1/blocks/{page}/children?page_size=100" + (f"&start_cursor={cursor}" if cursor else "")
    r = json.loads(ntn("api", q))
    blocks += r["results"]
    if not r.get("has_more"): break
    cursor = r["next_cursor"]

for b in blocks:
    rt = b.get(b["type"], {}).get("rich_text", [])
    text = "".join(t["plain_text"] for t in rt)
    m = re.fullmatch(r"IMGSLOT(\d+)", text.strip())
    if not m: continue
    cap, path = images[int(m[1])]
    # single_part: works on free workspaces (files up to 5 MB); `ntn files create` is multipart-only
    up = json.loads(ntn("api", "v1/file_uploads", "-X", "POST", "-d", json.dumps(
        {"mode": "single_part", "filename": path.name, "content_type": "image/png"})))
    ntn("api", f"v1/file_uploads/{up['id']}/send", "-X", "POST", "--file", str(path))
    child = {"type": "image", "image": {"type": "file_upload", "file_upload": {"id": up["id"]},
             "caption": [{"type": "text", "text": {"content": cap[:2000]}}]}}
    ntn("api", f"v1/blocks/{page}/children", "-X", "PATCH",
        "-d", json.dumps({"children": [child], "position": {"type": "after_block", "after_block": {"id": b["id"]}}}))
    ntn("api", f"v1/blocks/{b['id']}", "-X", "DELETE")
print(page)
