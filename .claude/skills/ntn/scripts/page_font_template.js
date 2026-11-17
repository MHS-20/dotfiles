// Sets the page font on a whole Notion page tree: the root page and every sub-page below it, found automatically.
// Use: open the root page on notion.so, F12 -> Console, type "allow pasting" by hand, paste this, Enter, then reload.
// Uses the web client's internal (unofficial) API with the logged-in session; it may stop working if Notion changes it.
(async () => {
  const FONT = "__FONT__";     // "default" | "serif" | "mono"
  const ROOT = "__ROOT__";     // page ID; empty = the page open in this tab
  const DRY_RUN = false;       // true = only list the pages it would change

  const hex = (ROOT || location.pathname).replace(/-/g, "").match(/[0-9a-f]{32}(?=[^0-9a-f]*$)/i);
  if (!hex) { console.error("No page ID: open the root page or set ROOT."); return; }
  const dash = h => `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
  const root = dash(hex[0].toLowerCase());

  const post = async (path, body) => {
    for (let t = 0; ; t++) {
      const r = await fetch("/api/v3/" + path, {
        method: "POST", credentials: "include",
        headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
      });
      if (r.ok) return r.json();
      if (r.status !== 429 || t > 5) throw new Error(path + " " + r.status);
      await new Promise(s => setTimeout(s, 2000 * (t + 1)));   // rate limited: back off
    }
  };
  const val = rec => rec?.value?.value ?? rec?.value;           // recordMap shape varies
  const fetchBlocks = async ids => {
    const out = {};
    for (let i = 0; i < ids.length; i += 100) {
      const chunk = ids.slice(i, i + 100);
      const res = await post("syncRecordValues", {
        requests: chunk.map(id => ({ pointer: { table: "block", id }, version: -1 })),
      });
      for (const id of chunk) out[id] = val(res.recordMap?.block?.[id]);
    }
    return out;
  };

  // Walk the tree: a page's `content` lists its child blocks; sub-pages are blocks of type "page"
  // (also when nested inside toggles or columns, so every block with content is descended into).
  const pages = [], seen = new Set([root]);
  let queue = [root], skippedDb = 0;
  const first = (await fetchBlocks([root]))[root];
  if (!first) { console.error("Root page not found or not accessible:", root); return; }
  pages.push(first);
  while (queue.length) {
    const parents = await fetchBlocks(queue);
    const childIds = [];
    for (const id of queue) for (const c of parents[id]?.content ?? []) if (!seen.has(c)) { seen.add(c); childIds.push(c); }
    const kids = await fetchBlocks(childIds);
    queue = [];
    for (const id of childIds) {
      const b = kids[id];
      if (!b || b.alive === false) continue;                       // deleted or not readable
      if (b.type === "page") pages.push(b);
      if (b.type?.startsWith("collection_view")) { skippedDb++; continue; } // databases: rows not walked
      if (b.content?.length) queue.push(id);
    }
    console.log(`found ${pages.length} pages so far`);
  }
  console.log(`${pages.length} pages under "${first.properties?.title?.[0]?.[0] ?? root}"` +
              (skippedDb ? ` (${skippedDb} databases skipped)` : ""));

  let ok = 0, same = 0, fail = 0;
  for (const b of pages) {
    const title = b.properties?.title?.[0]?.[0] ?? b.id;
    if ((b.format?.page_font ?? "default") === FONT) { same++; continue; }
    if (DRY_RUN) { console.log("would set", title); ok++; continue; }
    try {
      await post("saveTransactions", {
        requestId: crypto.randomUUID(),
        transactions: [{
          id: crypto.randomUUID(), spaceId: b.space_id,
          operations: [{ pointer: { table: "block", id: b.id, spaceId: b.space_id },
                         path: ["format", "page_font"], command: "set", args: FONT }],
        }],
      });
      ok++;
      if (ok % 25 === 0) console.log(`${ok} set`);
    } catch (e) { console.warn("error", title, e.message); fail++; }
  }
  console.log(`Done: ${ok} ${DRY_RUN ? "would change" : "set to " + FONT}, ${same} already ${FONT}, ${fail} errors. Reload to see it.`);
})();
