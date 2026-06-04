# Import Open Clip

**Script:** `import_open_clip.py` (+ `lib/`, `config/`)  
**Version:** 1.0 | **Flame:** 2027+  
**Context:** Batch (right-click on a Write File node)  
**Based on:** Michael Vaglienty's *Import Write Node* (PyFlame library, GPL-3.0)

## Description

Imports the open clip created by a selected **Write File** node into a Batch schematic reel (the `Renders` reel by default). Resolves the write node's `create_clip_path` tokens — including the Flame 2027 token-slicing syntax (e.g. `<shot name[0:-6]>`) — and sources `<version name>` / `<version>` from the node's own versioning settings.

## Usage

1. In Batch, right-click a **Write File** node.
2. Select **Import... > Import Open Clip to Batch**.

## Structure

This is a multi-file script and must be deployed as a folder (the main script does `from lib.pyflame_lib_import_open_clip import *`):

- `import_open_clip.py` — main script
- `lib/pyflame_lib_import_open_clip.py` — Michael Vaglienty's PyFlame library (GPL-3.0)
- `config/config.json` — stores the destination schematic reel name

See `import_open_clip_NOTES.md` for fork details, the token→source mapping, and live-API notes.

## Requirements

- Flame 2025.1+ (token slicing requires Flame 2027)
- The bundled `lib/` and `config/` folders — don't install the `.py` on its own
