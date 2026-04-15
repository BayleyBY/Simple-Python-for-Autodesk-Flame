# Merge Offline

**Script:** `_BB_merge_offline_008.py`  
**Version:** 6.0 | **Flame:** 2024+  
**Context:** Media Panel (right-click on sequence)

## Description

Automates merging an offline edit (AAF/XML/EDL) with a reference video into a single sequence ready for online comparison. This is a core conform/finishing workflow script.

## What It Does

1. Opens the selected sequence.
2. Moves all existing tracks up two layers (via `Nudge 1 Track Up` shortcut), leaving a blank top track.
3. Adds a stereo audio track for the reference audio.
4. Finds the matching reference clip (same name as the sequence + `_ref`) and overwrites it onto the bottom track and audio track.
5. Sets primary track (top) and secondary track (bottom) for A/B comparison.
6. Locks the reference video and audio tracks.
7. Clears in/out marks.
8. Adds virtual padding: head `59:59:00`, tail `+25 frames`.
9. Sets the top track gap to black and cuts it to picture-only range.
10. Moves the playhead to the start and frames the timeline.
11. Deletes the standalone `_ref` clip from the Media Panel.

## Prerequisites

- Import the AAF/XML/EDL to a sequence reel.
- Import the reference video to the **same** sequence reel and name it `<sequence_name>_ref`.
- The reference video must share the same start frame as the AAF/XML/EDL.
- Keyboard shortcuts for `Overwrite Edit` and `Swap Selected` must exist (even if unassigned to a key).

## Usage

1. Select the AAF/XML/EDL sequence in the Media Panel.
2. Right-click → **Sequence... > Merge Offline**

## Requirements

- Flame 2024+
