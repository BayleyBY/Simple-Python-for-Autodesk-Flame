# Merge Offline

**Script:** `merge_offline.py`  
**Version:** 1.0 | **Flame:** 2026+  
**Context:** Media Panel (right-click on sequence)

## Description

Automates merging an offline edit (AAF/XML/EDL) with a reference video into a single sequence ready for online comparison. This is a core conform/finishing workflow script.

## What It Does

1. Finds the matching reference clip (same name as the sequence + `_OFFLINE`). If it isn't found, the sequence is skipped untouched.
2. Opens the selected sequence.
3. Moves all existing tracks up two layers (via `Nudge 1 Track Up` shortcut), leaving a blank top track.
4. Adds a stereo audio track for the reference audio.
5. Overwrites the reference onto the bottom track and audio track.
6. Sets primary track (top) and secondary track (bottom) for A/B comparison.
7. Locks the reference video and audio tracks.
8. Clears in/out marks.
9. Adds virtual padding: head `59:59:00`, tail `+25 frames`.
10. Sets the top track gap to black and cuts it to picture-only range.
11. Moves the playhead to the start and frames the timeline.
12. Deletes the standalone `_OFFLINE` clip from the Media Panel.

## Prerequisites

- Import the AAF/XML/EDL to a sequence reel.
- Import the reference video to the **same** sequence reel and name it `<sequence_name>_OFFLINE`.
- The reference video must share the same start frame as the AAF/XML/EDL (no 2-pop offset).
- The default keyboard shortcut entries used by the script must still exist in the Keyboard Shortcut editor (even if unassigned to a key): `Nudge 1 Track Up`, `Nudge 1 Track Down`, `Overwrite Edit`, `Timeline Home`, `Set Focus on Topmost Visible Track`.

## Usage

1. Select the AAF/XML/EDL sequence in the Media Panel.
2. Right-click → **Sequence... > Merge Offline**

## Requirements

- Flame 2026+ (uses the `Set Focus on Topmost Visible Track` shortcut name introduced when Flame renamed `Set Focus on Top Visible Track`; on older Flame versions, edit the script to use the old name)
