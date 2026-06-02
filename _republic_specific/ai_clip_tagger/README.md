# AI Clip Tagger

> 🔒 **Workflow-specific — not submitted to the Logik Portal.** Uses a hard-coded facility export preset and poster-frames path, and an Anthropic API key on the local machine. Kept here under `_republic_specific/`. It still follows the repo's naming and docstring standards so it can be adapted.

**Script:** `ai_clip_tagger.py`  
**Version:** 1.0 | **Flame:** 2026.2+  
**Context:** Media Panel (right-click on clips)

## Description

Tags selected clips with AI-generated scene labels. For each clip it exports a single still frame, sends it to the Claude vision API, and applies the returned descriptive tags (`person`, `interior`, `office`, `food`, etc.) using Flame's native tag system (`clip.tags`).

## What it does

1. Exports the middle frame of each selected clip as a JPEG into a per-clip poster-frames folder.
2. Sends that frame to the Claude vision API (`claude-haiku-4-5-20251001`) with a tagging system prompt.
3. Parses the returned JSON array of tags and applies them to the clip.
4. Logs per-clip activity (including token usage and estimated cost) to a `<clip>_log.txt` beside each exported frame.

## Usage

1. Select one or more clips in the Media Panel.
2. Right-click → **AI... > Tag Clips with AI**

## Requirements

- Flame 2026.2+
- Anthropic API key saved as plain text at `~/.anthropic_api_key`
- JPG export preset at `/Volumes/Flame_Archive/SHARED/export/presets/file_sequence/JPG View Baked.xml`
- Facilis storage mounted at `/Volumes`; project nickname = partition name, project name = job folder
- Network access to `api.anthropic.com`
