---
name: thesis-diagrams
description: |-
  Author and compile thesis/paper figures from plain-text sources — TikZ,
  mermaid, graphviz, draw.io, SVG — into vector PDF for LaTeX and PNG for
  slides, using the bundled `figc` CLI. Use when creating, editing, or
  rebuilding a diagram, architecture figure, flowchart, pipeline, or block
  diagram for a thesis or paper, or when asked to turn a sketch or
  description into a figure.
license: MIT
metadata:
  audience: researchers
  domain: academic-figures
---

## What I do

Produce figures for a thesis as **text sources under version control**, compiled
to PDF and PNG by one command. No hand-placed screenshots, no binary blobs that
cannot be diffed or regenerated.

## Format choice — decide this first

| Use | When | Why |
| --- | --- | --- |
| **TikZ** (`.tex`) | every final figure in the thesis | Vector, and it uses the thesis's own fonts and math, so the figure does not look pasted in. Full control. Slowest to author. |
| **graphviz** (`.dot`) | graphs too large or too data-driven to place by hand | Automatic layout |
| **mermaid** (`.mmd`) | drafts, flowcharts, sequence diagrams while thinking | Fastest to write; distinctive house style that reads as "web tool" in a thesis |
| **draw.io** (`.drawio`) | a figure genuinely easier to drag than to code, or one inherited from a collaborator | GUI editing, XML on disk |
| **SVG** | figures exported from another tool | Convert once, do not hand-edit |

Default to TikZ for anything that ends up in the submitted document. Mermaid
and draw.io are for drafting; when a drafted figure is final, port it to TikZ.
Say so rather than silently shipping a mermaid render in a thesis.

## The CLI

`scripts/figc` — compiles sources to `<dir>/out/<name>.pdf` and `.png`.

```
figc                    # compile everything under ./figures (or $FIGDIR)
figc figures/arch.tex   # one file
figc -w                 # watch and rebuild on save
figc -f                 # force rebuild (default skips outputs newer than source)
figc -r 300             # PNG dpi (default 600)
figc --pdf-only         # skip PNG
figc -o build           # output directory
```

Exit status is nonzero if any figure failed; failures print the tectonic log
tail or the missing-tool install command and other figures still build.
Incremental by mtime, so a full `figc` on an unchanged tree is nearly free.

Symlink it onto PATH once: `ln -s ~/.claude/skills/thesis-diagrams/scripts/figc ~/.local/bin/figc`

## Layout convention

```
thesis/
  figures/
    architecture.tex      <- source, committed
    ablation.dot
    out/                  <- generated; gitignore it
      architecture.pdf    <- \includegraphics{figures/out/architecture}
      architecture.png
```

Add `figures/out/` to `.gitignore`. Sources are the artefact; outputs are
reproducible from `figc`.

## Authoring rules

- **Start from `templates/tikz-standalone.tex`.** It sets a `standalone`
  document class with a tight border, one named colour palette, and reusable
  `box` / `ghost` / `flow` / `lbl` styles.
- **Define styles once, reuse everywhere.** Every figure in the thesis draws
  from the same palette and the same node styles. Inconsistent figures are the
  most visible defect in a thesis; a reader notices mismatched arrowheads
  before they notice the content.
- **Never set an absolute figure width in the source.** Compile at natural
  size and scale at inclusion:
  `\includegraphics[width=\linewidth]{figures/out/arch}`. Scaling in TikZ
  distorts line weights and font sizes.
- **Match the body font.** Uncomment the matching font package in the
  template (`newtxtext` for a Times-like thesis, `lmodern` for default
  LaTeX). A figure in the wrong font is the giveaway that it came from
  elsewhere.
- **Position relationally**, with `positioning` (`right=of x`, `below=of y`),
  not absolute coordinates. Relational placement survives edits; hand-tuned
  coordinates do not.
- **Label edges** where the label carries information ($h_t$, a shape, a
  rate). Do not label an arrow "flows to".
- **Colour must survive greyscale printing.** Theses get printed. Vary
  lightness, not only hue, and never encode meaning in colour alone — add a
  line style, a fill pattern, or a label.
- **Keep one figure per file.** Multi-panel figures are assembled in LaTeX
  with `subcaption`, not inside one TikZ picture.
- Text in a figure should be no smaller than `\scriptsize` at final printed
  scale.

## Toolchain

Verified working on this machine with no further installs: **TikZ**, via
`tectonic` → PDF → `pdftocairo` → PNG. First compile downloads fonts and
packages (~20s); cached rebuilds are about one second. SVG conversion works
through `rsvg-convert`.

Optional, each needed only for its own format — `figc` names the install
command when a format is used without its tool:

| Need | Install |
| --- | --- |
| `.dot` graphviz | `pacman -S graphviz` |
| `.drawio` export | `pacman -S drawio-desktop` |
| better SVG→PDF, editing | `pacman -S inkscape` |
| `figc -w` watch mode | `pacman -S inotify-tools` |
| `.mmd` mermaid | none — runs via `npx`; `npm i -g @mermaid-js/mermaid-cli` to avoid the per-run fetch |

## Workflow

1. Pick the format from the table above; default TikZ.
2. Copy the template into `figures/<name>.tex` and write the figure.
3. `figc figures/<name>.tex`, then **look at the generated PNG** before
   reporting it done — a figure that compiles can still overlap, clip, or
   collide.
4. Include the **PDF**, not the PNG, in the LaTeX document.
5. Rebuild the whole set with `figc` before a submission build.

Never report a figure as finished without having viewed its output.
