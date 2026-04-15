# Remux to MP4

**Script:** `_BB_remux_to_mp4_002.py`  
**Version:** 1.0 | **Flame:** 2024+  
**Context:** Flame export hook (no right-click menu)  
**Modified from a script by:** Bob Maple

## Description

A Flame export hook that automatically remuxes any exported `.mov` to `.mp4` using ffmpeg when an export preset whose name matches `MP4_H264*` is used. This is a true remux (stream copy) — not a transcode — so it is fast and lossless for video. Audio is re-encoded to AAC 320k to ensure sync compatibility.

After a successful remux, the source `.mov` is deleted.

## How It Works

This script uses three Flame hook functions:

| Hook | Purpose |
|------|---------|
| `pre_export_asset` | Captures the resolved output file path |
| `pre_export` | Captures the name of the export preset used |
| `post_export_sequence` | Runs ffmpeg remux if preset matches `MP4_H264*` |

## Triggering

The hook fires automatically after any export using a preset whose filename starts with `MP4_H264`. No right-click menu is required.

## Installation

Place this script in your Flame hooks directory (typically `/opt/Autodesk/project/<project>/python/` or the shared hooks folder). It does not register a context menu — it runs passively as an export hook.

## Requirements

- Flame 2024+
- ffmpeg installed at `/usr/local/bin/ffmpeg`

## Related

See also `quick_posting_mp4` which bundles a similar remux step with a full posting export workflow.
