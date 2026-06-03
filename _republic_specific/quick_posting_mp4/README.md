# Quick Posting MP4

> 🔒 **Workflow-specific — not submitted to the Logik Portal.** This script is hard-wired to a specific facility setup (mounted Facilis partition paths, project naming convention, and a named export preset), so it is kept here under `_republic_specific/` rather than shared. It still follows the repo's naming and docstring standards so it can be adapted.

**Script:** `quick_posting_mp4.py`  
**Version:** 1.0 | **Flame:** 2024+  
**Context:** Media Panel (right-click on clip)

## Description

Exports selected clips straight to `.mp4` (via the posting preset) into the job's Postings folder. Designed for fast client review postings in an advertising/broadcast finishing environment.

After export, a shortened version of the destination path is copied to the clipboard for easy sharing via Slack.

## What It Does

1. Builds a time-stamped export path: `03_Exports/01_Postings/02_Online/<YY-MM-DD-HHmm>/` where minutes are rounded to the nearest 15-minute increment.
2. Exports the clip using the `ApprovalPosting_MP4_20Mbits.xml` preset (must exist at the path below) — this preset writes `.mp4` directly.
3. Navigates MediaHub to the export folder.
4. Copies a shortened path (everything after the job folder) to the clipboard.
5. Opens a Finder window at the export folder.

## Path Assumptions

- Facilis partitions mounted at `/Volumes`
- **Flame Project Nickname** = Facilis partition name (e.g. `Republic_2023_Q1`)
- **Flame Project Name** = Job folder name (e.g. `R2305590_Client_Project`)
- Export path template: `/Volumes/<ProjectNickName>/<ProjectName>/03_Exports/01_Postings/02_Online/<YY>-<MM>-<DD>-<Hour><Minute>/`

## Requirements

- Flame 2022+ (Flame must be able to export `.mp4` directly)
- Export preset at `/Volumes/Flame_Archive/SHARED/export/presets/movie_file/ApprovalPosting_MP4_20Mbits.xml`
- PySide6 or PySide2 (bundled with Flame)
