# Simple Python for Autodesk Flame

A collection of Python utility scripts for [Autodesk Flame](https://www.autodesk.com/products/flame/overview) — a professional visual effects and finishing system. Each script adds custom right-click context menus to Flame's various panels.

## Scripts

Each script lives in its own folder with a README explaining usage, prerequisites, and context menu locations.

### [Append Start Frame to Name](append_startframe_to_name/)
Appends the source start frame of a clip to the end of its name, zero-padded to 8 digits. Useful when exporting multiple clips with the same name — the frame number acts as a unique identifier to prevent files from overwriting each other.

### [Black Head and Tail](black_head_and_tail/)
Adds one second of virtual black to the head and tail of selected sequences by overwriting a "BLACK" clip from the desktop into the sequence at the correct edit points.

### [Cache Motion Vectors](cache_motion_vectors/)
In Batch, automatically builds the Action/Media node network needed to cache motion vectors for a selected clip node and caches them across the full clip duration.

### [Clip Path to Clipboard](clip_path_to_clipboard/)
Copies the source file path of selected clips to the clipboard. Works across Media Panel, Timeline, Batch, and MediaHub. Includes a shortened path option that strips the leading volume and project folders for cleaner Slack sharing.

### [Color Timewarp Shots](color_timewarp_shots/)
Scans all segments in selected sequences and colors any segment containing a Timewarp timeline effect dark red. Gives a quick visual overview of retimed shots during conform or finishing.

### [Create Marker](create_marker/) *(Deprecated — now a built-in Flame feature)*
Creates a clip-level or segment-level marker that spans the exact duration of the selected timeline segment. Two options: a standard clip marker or a segment marker, both sized to match the segment. This functionality is now built into Flame and this script is no longer needed.

### [Create Reel Group](create_reel_group/)
Creates a standardized Online Assemble reel group inside a selected library, pre-configured with `_Sources Sequence`, `Sources`, and `Conform` reels in the standard colors used for online finishing.

### [Delete Empty Tracks](delete_empty_tracks/)
Removes all empty video and audio tracks from selected sequences. Handles stereo pairs correctly — a stereo pair is only deleted if both channels are empty.

### [Freeze Frame Mux](freeze_frame_mux/)
In Batch, adds a Mux node after the selected node and configures it to freeze on the current playhead frame, with "Repeat First" before and "Repeat Last" after. Automatically connects matte/alpha outputs if present.

### [Merge Offline](merge_offline/)
Automates merging an AAF/XML/EDL sequence with a reference video for online comparison. Stacks the offline edit above the reference, sets primary/secondary tracks, locks the reference, adds virtual padding, and cleans up the reference clip from the Media Panel.

### [Open PSD in Photoshop](open_photoshop/)
Opens the source PSD file of a soft-imported clip in Photoshop (macOS only). Works from Timeline, Batch, Media Panel, and MediaHub. The context menu only appears when the selected clip is a `.psd` file.

### [Quick Posting MP4](quick_posting_mp4/)
Exports a selected clip to a time-stamped postings folder and immediately remuxes the output `.mov` to `.mp4` using ffmpeg. Copies a shortened path to the clipboard for sharing via Slack.

### [Ratio Bug Fix](ratio_bug_fix/)
Workaround for a Flame bug where segments with an Action timeline effect display the wrong size/ratio after conforming footage at a different resolution. Adds and immediately removes a Source Colour Mgmt effect to force Flame to re-evaluate the source resolution.

### [Remux to MP4](remux_to_mp4/)
A passive Flame export hook that automatically remuxes any exported `.mov` to `.mp4` using ffmpeg whenever an export preset matching `MP4_H264*` is used. No right-click menu — fires automatically after export.

### [Rename 9 and 12](rename_9_and_12/)
Truncates clip names to either 9 characters (FCB ID format) or 12 characters (AD-ID format) for broadcast TVC delivery. Also includes an option to remove the last 22 characters, useful for stripping suffixes added by Premiere XML fixer tools.

### [Set In/Out](set_in_out/)
Sets In/Out marks on selected clips for common delivery and approval workflows: Client Posting, Slated Approvals, Slated Delivery, OLV/Social, and Republic Master. Each preset is tuned for the standard sequence layout with slate at `59:53:00` and picture at `1:00:00:00`.

### [Start Project](start_project/)
Full new-project setup in one click. Cleans the desktop and creates standard reels, renames the library to match the project, creates an Online Assemble reel group, and copies standard job folder bookmarks into the project. Individual actions are also available separately.

### [Surround Sound Mute / Unmute](surround_sound_mute_unmute/)
Mutes or unmutes the first 6 audio tracks (a standard 5.1 surround layout) on all selected clips with a single right-click action.

### [Timesheet](timesheet/)
Work-in-progress timesheet script. Currently only a `.bak` file — no active version in this repo yet.

### [Update Slate Date](update_slate_date/)
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
