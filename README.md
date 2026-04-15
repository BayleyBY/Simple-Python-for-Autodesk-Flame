# Simple Python for Autodesk Flame

A collection of Python utility scripts for [Autodesk Flame](https://www.autodesk.com/products/flame/overview) — a professional visual effects and finishing system. Each script adds custom right-click context menus to Flame's various panels.

## Scripts

Each script lives in its own folder with a README explaining usage, prerequisites, and context menu locations.

| Folder | Script | Panel | Description |
|--------|--------|-------|-------------|
| [`append_startframe_to_name`](append_startframe_to_name/) | `_BB_append_startframe_to_name_001.py` | Media Panel | Appends the source start frame to the clip name as a unique identifier |
| [`black_head_and_tail`](black_head_and_tail/) | `_BB_black_head_and_tail_001.py` | Media Panel | Adds 1 second of black to the head and tail of sequences |
| [`cache_motion_vectors`](cache_motion_vectors/) | `_BB_cache_motion_vectors_001.py` | Batch | Builds Action/Media node network and caches motion vectors |
| [`clip_path_to_clipboard`](clip_path_to_clipboard/) | `_BB_clip_path_to_clipboard_for_slack_001.py` | Media Panel / Timeline / Batch / MediaHub | Copies clip file path to clipboard; shortened path option for Slack sharing |
| [`color_timewarp_shots`](color_timewarp_shots/) | `_BB_color_timewarp_shots_001.py` | Media Panel | Colors all segments containing a Timewarp effect dark red |
| [`create_marker`](create_marker/) | `_BB_create_marker_001.py` | Timeline | Creates a clip or segment marker spanning the selected segment's duration |
| [`create_reel_group`](create_reel_group/) | `_BB_create_reel_group_002.py` | Media Panel | Creates a pre-colored Online Assemble reel group in a library |
| [`delete_empty_tracks`](delete_empty_tracks/) | `_BB_delete_empty_tracks_001.py` | Media Panel | Removes all empty video and audio tracks from sequences |
| [`freeze_frame_mux`](freeze_frame_mux/) | `_BB_freeze_frame_mux_001.py` | Batch | Adds a Mux node after the selected node and freezes on the current frame |
| [`merge_offline`](merge_offline/) | `_BB_merge_offline_008.py` | Media Panel | Merges an AAF/XML/EDL with a reference video into a comparison sequence |
| [`open_photoshop`](open_photoshop/) | `_BB_open_photoshop_007.py` | Timeline / Batch / Media Panel / MediaHub | Opens a soft-linked PSD file in Photoshop |
| [`quick_posting_mp4`](quick_posting_mp4/) | `_BB_quick_posting_mp4_004.py` | Media Panel | Exports clip to dated postings folder and remuxes to MP4 via ffmpeg |
| [`ratio_bug_fix`](ratio_bug_fix/) | `_BB_ratio_bug_fix_001.py` | Timeline | Fixes wrong size/ratio on Action-effected segments after AAF/XML conform |
| [`remux_to_mp4`](remux_to_mp4/) | `_BB_remux_to_mp4_002.py` | Export hook | Auto-remuxes `.mov` exports to `.mp4` when using `MP4_H264*` presets |
| [`rename_9_and_12`](rename_9_and_12/) | `_BB_rename_9_and_12_001.py` | Media Panel | Truncates clip names to 9 (FCB ID) or 12 (AD-ID) characters for broadcast delivery |
| [`set_in_out`](set_in_out/) | `_BB_set_in_out_005.py` | Media Panel | Sets In/Out marks for various delivery types: posting, slated, OLV, broadcast |
| [`start_project`](start_project/) | `_BB_start_project_006.py` | Media Panel | Full new-project setup: desktop, library, reel groups, and bookmarks |
| [`surround_sound_mute_unmute`](surround_sound_mute_unmute/) | `_BB_surround_sound_mute_and_unmute.py` | Media Panel | Mutes or unmutes the first 6 audio tracks (5.1 surround) on selected clips |
| [`timesheet`](timesheet/) | `_BB_timesheet_008.py.bak` | — | Work-in-progress timesheet script (backup only) |
| [`update_slate_date`](update_slate_date/) | `_BB_update_slate_date_005.py` | Media Panel | Updates Burn-in Metadata effects in sequences to show the current date |

## Installation

Copy the `.py` script file from any folder into your Flame Python scripts directory:

```
/opt/Autodesk/project/<project_name>/python/
```

Or use the shared hooks directory for scripts that should be available across all projects. Flame will auto-discover scripts placed in these locations and add them to the right-click menus on the next launch (or after reloading scripts).

## Requirements

- Autodesk Flame 2020 or later (specific version requirements listed per script)
- macOS (some scripts use macOS-specific tools like `open` and `ffmpeg`)
- ffmpeg at `/usr/local/bin/ffmpeg` (required by `quick_posting_mp4` and `remux_to_mp4`)
