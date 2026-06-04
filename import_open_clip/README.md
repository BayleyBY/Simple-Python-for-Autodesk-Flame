# Import Open Clip

**Script:** `import_open_clip.py`  
**Version:** 1.0 | **Flame:** 2027+  
**Context:** Batch (right-click on a Write File node)  
**Originally based on:** Michael Vaglienty's *Import Write Node*

## Description

Imports the open clip created by a selected **Write File** node into a Batch schematic reel (the `Renders` reel by default). Resolves the write node's `create_clip_path` tokens — including the Flame 2027 token-slicing syntax (e.g. `<shot name[0:-6]>`) — and sources `<version name>` / `<version>` from the node's own versioning settings.

## Usage

1. In Batch, right-click a **Write File** node.
2. Select **Import... > Import Open Clip to Batch**.

## Configuration

The destination schematic reel is set by the `SCHEMATIC_REEL` constant near the top of the script (defaults to `Renders`). Edit it to target a different reel.

## Requirements

- Flame 2025.1+ (token slicing requires Flame 2027)
- Single self-contained `.py` file — no bundled library or config folders.

See `import_open_clip_NOTES.md` for the token→source mapping and live-API notes.
