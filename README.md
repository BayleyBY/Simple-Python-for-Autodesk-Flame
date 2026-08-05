# Simple Python for Autodesk Flame

A collection of Python utility scripts for [Autodesk Flame](https://www.autodesk.com/products/flame/overview) — a professional visual effects and finishing system. Each script adds custom right-click context menus to Flame's various panels.

## Scripts

Each script lives in its own folder with a README explaining usage, prerequisites, and context menu locations.

### [AI Clip Tagger](_republic_specific/ai_clip_tagger/) *(Workflow-specific — not on Logik)*
Tags selected clips with AI-generated scene labels (person, interior, office, etc.) by exporting a still frame from each clip and sending it to the Claude vision API. Tags are applied with Flame's native tag system. Requires an Anthropic API key.

### [Alternating Colors](alternating_colors/)
Applies an alternating light/dark colour scheme to a group of same-type items (clips, reels, folders, etc.) selected in the Media Panel.

### [Append Start Frame to Name](append_start_frame_to_name/)
Appends the source start frame of a clip to the end of its name, zero-padded to 8 digits. Useful when exporting multiple clips with the same name — the frame number acts as a unique identifier to prevent files from overwriting each other.

### [BB TVC Timecode Checker](bb_tvc_timecode_checker/)
Checks selected clips or sequences for broadcast TVC delivery: whether the record timecode starts at `01:00:00:00` — or at a recognized black head/tail (`59:59:00`) or slate (`59:50:00` / `59:53:00`) lead-in — and whether the duration is a standard commercial length (6s, 15s, 30s, 60s, 90s) once the lead-in is accounted for. Assumed layouts are flagged for visual confirmation.

### [Black Head and Tail](black_head_and_tail/)
Adds one second of virtual black to the head and tail of selected sequences. A temporary black source is generated automatically — nothing needs to be set up on the desktop beforehand — and the black handles are added without rippling or shifting existing content.

### [Cache Motion Vectors](cache_motion_vectors/)
In Batch, automatically builds the Action/Media node network needed to cache motion vectors for a selected clip node and caches them across the full clip duration.

### [Clip Path to Clipboard](clip_path_to_clipboard/)
Copies the source file path of selected clips to the clipboard. Works across Media Panel, Timeline, Batch, and MediaHub. Includes a shortened path option that strips the leading volume and project folders for cleaner Slack sharing.

### [Color Shots by Effect](color_shots_by_effect/)
Colors all segments containing a chosen timeline effect (Action, Image, Blur, Timewarp, etc.). Scans the selected sequences for the effect types actually present, then lets you pick one plus a color — nine presets or a custom color picker. Locked segments are skipped and reported. Generalized version of Color Timewarp Shots.

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

### [Import Open Clip](import_open_clip/)
Imports the open clip created by a selected Write File node into a Batch schematic reel. Resolves the write node's path tokens (including Flame 2027 token-slicing) and the node's own versioning. Single self-contained script, originally based on Michael Vaglienty's Import Write Node.

### [Merge Offline](merge_offline/)
Automates merging an AAF/XML/EDL sequence with a reference video (found on the same reel by an `offline`/`ref` keyword or fuzzy name match) for online comparison. Stacks the offline edit above the reference, sets primary/secondary tracks, locks the reference, adds virtual padding, and cleans up the reference clip from the Media Panel.

### [Move Playhead](move_playhead/)
Moves the playhead of all selected clips or sequences to an absolute record timecode — presets for `00:59:53:00` and `01:00:00:00`, plus a custom timecode dialog. The playhead can be parked before the first frame of the sequence, useful for preparing slate insertions at standard broadcast lead-in positions.

### [New Project Setup](new_project_setup/)
Configurable one-click new-project setup. On first use, a setup window asks how your projects should be laid out — desktop reels, library naming, an online reel group, and a bookmarks template file — and saves the answers next to the script. Each action (Clean Desktop, Clear and Rename Library, Create ReelGroup for Online, Create Standard Project Bookmarks, or All The Things) then runs with your saved settings, changeable anytime via Setup...

### [Open in Photoshop](open_in_photoshop/)
Opens the source file of a soft-imported still image (PSD, PNG, JPEG, TIFF, and other Photoshop-friendly formats) in Photoshop — targeted by bundle id, so Photoshop need not be the default app (macOS only). Works from Timeline, Batch, Media Panel, and MediaHub. For frame sequences, the frame the playhead is parked on opens (Timeline / Media Panel); elsewhere the first frame. Replaces the older *Open PSD in Photoshop*.

### [Quick Posting Aspect Ratios](_republic_specific/quick_posting_aspect_ratios/) *(Workflow-specific — not on Logik)*
Exports selected clips to social aspect ratios (1x1, 9x16, 4x5), picking the export preset from each clip name's trailing suffix. Exports to the same dated postings folder as Quick Posting MP4, then copies a shortened path and opens Finder there.

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

### [Select Connected in Media Panel](select_connected_in_media_panel/)
Adds a Timeline menu that finds the Media Panel clips connected to the focused segment, expands their reels and selects them — with options to colour the connected clips green for visual tracking and to clear that colour afterwards.

### [Set In Out](_republic_specific/set_in_out/) *(Workflow-specific — not on Logik)*
Sets In/Out marks on selected clips for common delivery and approval workflows: Client Posting, Slated Approvals, Slated Delivery, OLV/Social, and Republic Master. Each preset is tuned for the standard sequence layout with slate at `59:53:00` and picture at `1:00:00:00`.

### [Start Project](_republic_specific/start_project/) *(Workflow-specific — not on Logik)*
Full new-project setup in one click. Cleans the desktop and creates standard reels, renames the library to match the project, creates an Online Assemble reel group, and copies standard job folder bookmarks into the project. Individual actions are also available separately.

### [Surround Sound Mute / Unmute](surround_sound_mute_unmute/)
Mutes or unmutes the first 6 audio tracks (a standard 5.1 surround layout) on all selected clips with a single right-click action.

### [Timesheet](_deprecated/timesheet/) *(Deprecated)*
Work-in-progress timesheet script. Currently only a `.bak` file — no active version in this repo yet.

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
- ffmpeg at `/usr/local/bin/ffmpeg` (only required by the deprecated `remux_to_mp4`)
