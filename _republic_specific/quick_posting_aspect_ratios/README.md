# Quick Posting Aspect Ratios

> 🔒 **Workflow-specific — not submitted to the Logik Portal.** Hard-wired to a Republic Editorial path layout, named aspect-ratio export presets, and a `/Volumes` mount. Kept here under `_republic_specific/`. It still follows the repo's naming and docstring standards so it can be adapted.

**Script:** `quick_posting_aspect_ratios.py`  
**Version:** 1.0 | **Flame:** 2024+  
**Context:** Media Panel (right-click on clips)

## Description

Exports selected clips to social aspect ratios, choosing the export preset from each clip name's trailing suffix. Uses the same dated postings folder (rounded to the nearest 15 minutes) as [Quick Posting MP4](../quick_posting_mp4/).

| Clip name suffix | Export preset |
|------------------|---------------|
| `1x1` | `Posting_16x9_to_1x1.xml` |
| `9x16` | `Posting_16x9_to_9x16.xml` |
| `4x5` | `Posting_16x9_to_4x5.xml` |

Clips whose names don't end with a recognized suffix are skipped with a console warning.

## What it does

1. Builds the dated export path (`03_Exports/01_Postings/02_Online/<YY-MM-DD-HHmm>/`).
2. Exports each clip with the preset matched to its name suffix.
3. Navigates MediaHub to the export folder, copies a shortened path to the clipboard, and opens a Finder window there.

## Usage

1. Name clips with a trailing aspect-ratio suffix (e.g. `MySpot_1x1`).
2. Select them in the Media Panel.
3. Right-click → **Export... > Quick Posting — Social Aspect Ratios**

## Requirements

- Flame 2022+
- PySide6 or PySide2 (bundled with Flame)
- Aspect-ratio export presets in `/Volumes/Flame_Archive/SHARED/export/presets/movie_file/`
- Facilis storage mounted at `/Volumes`; project nickname = partition, project name = job folder
