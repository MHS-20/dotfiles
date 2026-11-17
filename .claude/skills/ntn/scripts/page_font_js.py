#!/usr/bin/env python3
"""Generate a browser-console script that sets the page font on a whole Notion page tree.

Usage: python3 -I page_font_js.py [serif|default|mono] [root-page-id-or-url] [out.js]
The script finds the sub-pages itself, in the browser: it walks the tree from the root page
(or, with no root given, from the page open in the tab where it is pasted). Nothing is listed
here. The public API has no font field, so the JS uses the web client's internal API
(/api/v3/syncRecordValues + saveTransactions) with the user's logged-in session.
"""
import os, re, sys

font = sys.argv[1] if len(sys.argv) > 1 else "serif"
if font not in ("serif", "default", "mono"):
    sys.exit(__doc__)
root = ""
if len(sys.argv) > 2 and sys.argv[2]:
    m = re.findall(r"[0-9a-f]{32}", sys.argv[2].lower().replace("-", ""))
    if not m:
        sys.exit("no 32-hex page ID in " + sys.argv[2])
    root = m[-1]
out = sys.argv[3] if len(sys.argv) > 3 else "notion-font.js"
js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "page_font_template.js")).read()
open(out, "w").write(js.replace("__FONT__", font).replace("__ROOT__", root))
print(f"font={font} root={root or '(page open in the tab)'} -> {out}")
