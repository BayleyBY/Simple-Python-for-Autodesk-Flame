# Simple Python for Autodesk Flame

A collection of Python utility scripts for [Autodesk Flame](https://www.autodesk.com/products/flame/overview) — a professional visual effects and finishing system. Each script adds custom right-click context menus to Flame's various panels.

## Scripts

Each script lives in its own folder with a README explaining usage, prerequisites, and context menu locations.

### [AI Clip Tagger](_republic_specific/ai_clip_tagger/) *(Workflow-specific — not on Logik)*
Tags selected clips with AI-generated scene labels (person, interior, office, etc.) by exporting a still frame from each clip and sending it to the Claude vision API. Tags are applied with Flame's native tag system. Requires an Anthropic API key.

### [Append Start Frame to Name](append_start_frame_to_name/)
Appends the source start frame of a clip to the end of its name, zero-padded to 8 digits. Useful when exporting multiple clips with the same name — the frame number acts as a unique identifier to prevent files from overwriting each other.

### [Black Head and Tail](black_head_and_tail/)
Adds one second of virtual black to the head and tail of selected sequences. A temporary black source is generated automatically — nothing needs to be set up on the desktop beforehand — and the black handles are added without rippling or shifting existing content.

### [Cache Motion Vectors](cache_motion_vectors/)
In Batch, automatically builds the Action/Media node network needed to cache motion vectors for a selected clip node and caches them across the full clip duration.

### [Clip Path to Clipboard](clip_path_to_clipboard/)
Copies the source file path of selected clips to the clipboard. Works across Media Panel, Timeline, Batch, and MediaHub. Includes a shortened path option that strips the leading volume and project folders for cleaner Slack sharing.

### [Color Timewarp Shots](color_timewarp_shots/)
Scans all segments in selected sequences and colors any segment containing a Timewarp timeline effect dark red. Gives a quick visual overview of retimed shots during conform or finishing.

### [Create Marker](_deprecated/create_marker/) *(Deprecated — now a built-in Flame feature)*
Creates a clip-level or segment-level marker that spans the exact duration of the selected timeline segment. Two options: a standard clip marker or a segment marker, both sized to match the segment. This functionality is now built into Flame and this script is no longer needed.

### [Create Reel Group](create_reel_group/)
Creates a standardized Online Assemble reel group inside a selected library, pre-configured with `_Sources Sequence`, `Sources`, and `Conform` reels in the standard colors used for online finishing.

### [Delete Empty Tracks](delete_empty_tracks/)
Removes all empty video and audio tracks from selected sequences. Handles stereo pairs correctly — a stereo pair is only deleted if both channels are empty.

### [Freeze Frame Mux](_deprecated/freeze_frame_mux/) *(Deprecated)*
In Batch, adds a Mux node after the selected node and configures it to freeze on the current playhead frame, with "Repeat First" before and "Repeat Last" after. Automatically connects matte/alpha outputs if present.

### [Merge Offline](_deprecated/merge_offline/) *(Deprecated)*
Automates merging an AAF/XML/EDL sequence with a reference video for online comparison. Stacks the offline edit above the reference, sets primary/secondary tracks, locks the reference, adds virtual padding, and cleans up the reference clip from the Media Panel.

### [Open PSD in Photoshop](open_psd_in_photoshop/)
Opens the source PSD file of a soft-imported clip in Photoshop (macOS only). Works from Timeline, Batch, Media Panel, and MediaHub. The context menu only appears when the selected clip is a `.psd` file.

### [Quick Posting MP4](_republic_specific/quick_posting_mp4/) *(Workflow-specific — not on Logik)*
Exports a selected clip to a time-stamped postings folder and immediately remuxes the output `.mov` to `.mp4` using ffmpeg. Copies a shortened path to the clipboard for sharing via Slack.

### [Ratio Bug Fix](_deprecated/ratio_bug_fix/) *(Deprecated)*
Workaround for a Flame bug where segments with an Action timeline effect display the wrong size/ratio after conforming footage at a different resolution. Adds and immediately removes a Source Colour Mgmt effect to force Flame to re-evaluate the source resolution.

### [Remux to MP4](_deprecated/remux_to_mp4/) *(Deprecated)*
A passive Flame export hook that automatically remuxes any exported `.mov` to `.mp4` using ffmpeg whenever an export preset matching `MP4_H264*` is used. No right-click menu — fires automatically after export.

### [Rename Keep AD-ID](rename_keep_ad_id/)
Truncates clip names to either 9 characters (older ISCI ID format) or 12 characters (AD-ID format) for broadcast TVC delivery. Also includes an option to strip the suffix added by Premiere XML fixer tools (removes the last 22 characters).

### [SammieRoto Round Trip](_republic_specific/sammieroto_round_trip/) *(Workflow-specific — not on Logik)*
Exports selected clips or batch clip nodes as JPEG sequences, opens them in Sammie Roto 2.0 for AI rotoscoping, then imports the result back into the Flame Batch. Hard-wired to a Republic Editorial path layout; edit the CONFIG block before use.

### [Segment Color to Clip Color](segment_color_to_clip_color/)
Copies the colour label of the first segment in a clip up to the clip level. Useful in a color grading workflow for seeing at a glance that source clips are connected to their segments in the sequence.

### [Set In Out](_republic_specific/set_in_out/) *(Workflow-specific — not on Logik)*
Sets In/Out marks on selected clips for common delivery and approval workflows: Client Posting, Slated Approvals, Slated Delivery, OLV/Social, and Republic Master. Each preset is tuned for the standard sequence layout with slate at `59:53:00` and picture at `1:00:00:00`.

### [Start Project](_republic_specific/start_project/) *(Workflow-specific — not on Logik)*
Full new-project setup in one click. Cleans the desktop and creates standard reels, renames the library to match the project, creates an Online Assemble reel group, and copies standard job folder bookmarks into the project. Individual actions are also available separately.

### [Surround Sound Mute / Unmute](surround_sound_mute_unmute/)
Mutes or unmutes the first 6 audio tracks (a standard 5.1 surround layout) on all selected clips with a single right-click action.

### [Timesheet](_deprecated/timesheet/) *(Deprecated)*
Work-in-progress timesheet script. Currently only a `.bak` file — no active version in this repo yet.

### [TVC Timecode Checker](bb_tvc_timecode_checker/)
Checks selected clips or sequences for broadcast TVC delivery: whether the record timecode starts at `01:00:00:00` and whether the duration is a standard commercial length (6s, 15s, 30s, 60s, 90s).

### [Update Slate Date](_deprecated/update_slate_date/) *(Deprecated)*
Updates all Burn-in Metadata timeline effects in selected sequences to show the current date. Designed for refreshing slate dates before a new round of deliveries.

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
