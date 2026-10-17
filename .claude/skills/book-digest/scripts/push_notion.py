#!/usr/bin/env python3
"""Create a Notion child page from a markdown file.

Usage: NOTION_TOKEN=... push_notion.py <parent-page-url-or-id> <file.md>
Handles headings, paragraphs, bullets, numbered lists, quotes, code blocks,
<details> (as a toggle), ![alt](path) images (local files are uploaded via
the File Upload API, URLs are embedded; each is centered at IMAGE_WIDTH of the page) and **bold**/`code` inline. Stdlib only.
"""
import json
import mimetypes
import os
import uuid
import re
import sys
import urllib.error
import urllib.request

API = "https://api.notion.com/v1"
MAX_TEXT = 2000
IMAGE_WIDTH = 0.80  # share of the page width; images sit in a centered column (Notion has no image width in its API)


def request(method, path, body, raw=None, content_type="application/json"):
    req = urllib.request.Request(
        path if path.startswith("http") else API + path, method=method,
        data=raw if raw is not None else json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {os.environ['NOTION_TOKEN']}",
                 "Notion-Version": "2022-06-28", "Content-Type": content_type})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"Notion API {e.code}: {e.read().decode()}")


def page_id(url):
    match = re.search(r"([0-9a-f]{32})(?:\?|$)", url.replace("-", ""))
    if not match:
        sys.exit(f"Can't find a page id in {url}")
    return match.group(1)


def rich(text):
    parts = []
    for token in re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", text):
        if not token:
            continue
        ann = {}
        if token.startswith("**"):
            token, ann = token[2:-2], {"bold": True}
        elif token.startswith("`"):
            token, ann = token[1:-1], {"code": True}
        for i in range(0, len(token), MAX_TEXT):
            parts.append({"type": "text", "text": {"content": token[i:i + MAX_TEXT]}, "annotations": ann})
    return parts


def upload(path):
    """Upload a local file to Notion and return its file_upload id."""
    name = os.path.basename(path)
    mime = mimetypes.guess_type(name)[0] or "application/octet-stream"
    created = request("POST", "/file_uploads", {"filename": name, "content_type": mime})
    boundary = uuid.uuid4().hex
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{name}\"\r\n"
            f"Content-Type: {mime}\r\n\r\n").encode() + open(path, "rb").read() + f"\r\n--{boundary}--\r\n".encode()
    request("POST", created["upload_url"], None, raw=body,
            content_type=f"multipart/form-data; boundary={boundary}")
    return created["id"]


def image_block(src, caption, base_dir):
    if re.match(r"https?://", src):
        image = {"type": "external", "external": {"url": src}}
    else:
        image = {"type": "file_upload", "file_upload": {"id": upload(os.path.join(base_dir, src))}}
    image["caption"] = rich(caption)
    return centered({"object": "block", "type": "image", "image": image})


def centered(content, width=IMAGE_WIDTH):
    """Wrap a block in a three-column layout so it takes `width` of the page, centered."""
    if width >= 1:
        return content
    side = (1 - width) / 2
    spacer = {"object": "block", "type": "paragraph", "paragraph": {"rich_text": []}}
    column = lambda ratio, child: {"object": "block", "type": "column", "column": {"width_ratio": ratio, "children": [child]}}
    return {"object": "block", "type": "column_list", "column_list": {
        "children": [column(side, spacer), column(width, content), column(side, spacer)]}}


def block(kind, text, **extra):
    return {"object": "block", "type": kind, kind: {"rich_text": rich(text), **extra}}


def code_block(lines, lang):
    text = "\n".join(lines)
    chunks = [text[i:i + MAX_TEXT] for i in range(0, len(text), MAX_TEXT)] or [""]
    return {"object": "block", "type": "code", "code": {
        "language": lang or "plain text",
        "rich_text": [{"type": "text", "text": {"content": c}} for c in chunks]}}


def parse(md, base_dir="."):
    blocks, target, lines, i = [], None, md.splitlines(), 0
    out = lambda b: (target if target is not None else blocks).append(b)
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            lang, body = line[3:].strip(), []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            out(code_block(body, lang))
        elif m := re.match(r"<details><summary>(.*)</summary>", line):
            toggle = block("toggle", m.group(1), children=[])
            blocks.append(toggle)
            target = toggle["toggle"]["children"]
        elif line.startswith("</details>"):
            target = None
        elif m := re.match(r"!\[(.*?)\]\((.+?)\)\s*$", line.strip()):
            out(image_block(m.group(2), m.group(1), base_dir))
        elif m := re.match(r"(#{1,6}) (.*)", line):
            # '#' is the page title, so body sections start at '##' = heading_2; Notion's smallest is heading_4
            out(block(f"heading_{min(len(m.group(1)), 4)}", m.group(2)))
        elif line.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> ").rstrip())
                i += 1
            out(block("quote", "\n".join(quote).strip()))
            continue
        elif m := re.match(r"\s*[-*] (.*)", line):
            out(block("bulleted_list_item", m.group(1)))
        elif m := re.match(r"\s*\d+\. (.*)", line):
            out(block("numbered_list_item", m.group(1)))
        elif line.strip():
            para = [line]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"(#|>|```|!\[|\s*[-*] |\s*\d+\. |<)", lines[i + 1]):
                i += 1
                para.append(lines[i])
            out(block("paragraph", " ".join(para)))
        i += 1
    return blocks


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    if "NOTION_TOKEN" not in os.environ:
        sys.exit("NOTION_TOKEN is not set")
    parent, path = sys.argv[1:]
    md = open(path, encoding="utf-8").read()
    title_match = re.match(r"# (.*)\n", md)
    title = title_match.group(1) if title_match else os.path.basename(path)
    blocks = parse(md[title_match.end():] if title_match else md, os.path.dirname(os.path.abspath(path)))

    page = request("POST", "/pages", {
        "parent": {"page_id": page_id(parent)},
        "properties": {"title": {"title": [{"text": {"content": title}}]}},
        "children": blocks[:100]})
    for start in range(100, len(blocks), 100):
        request("PATCH", f"/blocks/{page['id']}/children", {"children": blocks[start:start + 100]})
    print(page["url"])


if __name__ == "__main__":
    main()
