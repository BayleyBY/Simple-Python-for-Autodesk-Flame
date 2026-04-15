# Quick Posting MP4

**Script:** `_BB_quick_posting_mp4_004.py`  
**Version:** 1.0 | **Flame:** 2024+  
**Context:** Media Panel (right-click on clip)

## Description

Exports selected clips to the job's Postings folder and automatically remuxes the output `.mov` to `.mp4` using ffmpeg. Designed for fast client review postings in an advertising/broadcast finishing environment.

After export, a shortened version of the destination path is copied to the clipboard for easy sharing via Slack.

## What It Does

1. Builds a time-stamped export path: `03_Exports/01_Postings/02_Online/<YY-MM-DD-HHmm>/` where minutes are rounded to the nearest 15-minute increment.
2. Exports the clip using the `Quick_Posting_MP4.xml` preset (must exist in Flame's shared export presets).
3. Navigates MediaHub to the export folder.
4. Copies a shortened path (everything after the job folder) to the clipboard.
5. Uses a `post_export_sequence` hook to remux the `.mov` to `.mp4` with ffmpeg (`-codec:v copy`, `-codec:a aac 320k`), then deletes the source `.mov`.

## Path Assumptions

- Facilis partitions mounted at `/Volumes`
- **Flame Project Nickname** = Facilis partition name (e.g. `Republic_2023_Q1`)
- **Flame Project Name** = Job folder name (e.g. `R2305590_Client_Project`)
- Export path template: `/Volumes/<ProjectNickName>/<ProjectName>/03_Exports/01_Postings/02_Online/<YY>-<MM>-<DD>-<Hour><Minute>/`

## Requirements

- Flame 2022+
- ffmpeg installed at `/usr/local/bin/ffmpeg`
- Export preset at `/opt/Autodesk/shared/export/presets/movie_file/Quick_Posting_MP4.xml`
- PySide2 (bundled with Flame)

## Related

See also `remux_to_mp4` for a general-purpose remux hook that triggers on any export preset matching `MP4_H264*`.
