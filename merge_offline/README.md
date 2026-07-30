# Merge Offline

**Script:** `merge_offline.py`  
**Version:** 1.0 | **Flame:** 2026+  
**Context:** Media Panel (right-click on sequence)

## Description

Automates merging an offline edit (AAF/XML/EDL) with a reference video into a single sequence ready for online comparison. This is a core conform/finishing workflow script.

## What It Does

1. Finds the reference clip on the same reel as the sequence using a layered lookup:
   - Any clip whose name contains `offline`, `reference`, or the word `ref` (case-insensitive). If several match, the one named most like the sequence wins.
   - Otherwise, the clip whose name is most similar to the sequence name (fuzzy match — e.g. `JOB123_ONLINE` finds `JOB123_v12`).
   - If neither layer finds a plausible reference, the sequence is skipped untouched. All skipped sequences are listed in a single dialog after everything else has merged.
2. Opens the selected sequence.
3. Detects a 2-pop / slate lead-in (a start inside the last minute before the hour, e.g. `59:58:00`) and lifts it out of both the sequence and the reference after the overwrite — nothing ripples, so all content keeps its timecode and the program stays on the hour. Sequences already starting on the hour are untouched.
4. Moves all existing tracks up two layers (via `Nudge 1 Track Up` shortcut), leaving a blank top track. If the nudge has no effect (seen on a 60 fps sequence), the sequence is skipped safely before anything is modified further.
5. Adds a stereo audio track for the reference audio.
6. Overwrites the reference onto the bottom track and audio track.
7. Sets primary track (top) and secondary track (bottom) for A/B comparison.
8. Locks the reference video and audio tracks.
9. Clears in/out marks.
10. Adds one second of virtual padding to head and tail, derived from the sequence's own frame rate and start timecode (any rate and start TC work — nothing is hardcoded).
11. Sets the top track gap to black and cuts it to picture-only range.
12. Moves the playhead to the start and frames the timeline.
13. Deletes the standalone reference clip from the Media Panel.

## Prerequisites

- Import the AAF/XML/EDL to a sequence reel.
- Import the reference video to the **same** sequence reel. Naming it with `offline`, `ref`, or `reference` in the name (e.g. `<sequence_name>_OFFLINE`) guarantees it is found; otherwise its name must closely resemble the sequence name.
- The reference video must share the same start frame as the AAF/XML/EDL (no 2-pop offset).
- The default keyboard shortcut entries used by the script must still exist in the Keyboard Shortcut editor (even if unassigned to a key): `Nudge 1 Track Up`, `Nudge 1 Track Down`, `Overwrite Edit`, `Timeline Home`, `Set Focus on Topmost Visible Track`.

## Usage

14. Select the AAF/XML/EDL sequence in the Media Panel.
15. Right-click → **Sequence... > Merge Offline**

## Requirements

- Flame 2026+ (uses the `Set Focus on Topmost Visible Track` shortcut name introduced when Flame renamed `Set Focus on Top Visible Track`; on older Flame versions, edit the script to use the old name)
