# Black Head and Tail

**Script:** `_BB_black_head_and_tail_001.py`  
**Version:** 1.5 | **Flame:** 2022.1+  
**Context:** Media Panel (right-click on sequence)

## Description

Adds one second of virtual black to both the head and tail of selected sequences by overwriting a "BLACK" clip from the desktop into the sequence at the correct edit points.

- **Head black:** inserted at `59:59:00 – 1:00:00:00`
- **Tail black:** inserted immediately after the last frame

## Prerequisites

- A **Colour Source (Black)** clip named exactly `BLACK` must exist on the desktop with a 1-second duration.
- Sequences must have the correct **track patching** set before running (Python cannot control patching).

## Usage

1. Place a 1-second black Colour Source named `BLACK` on the desktop.
2. Set track patching on your sequences.
3. Select one or more sequences in the Media Panel.
4. Right-click → **Sequence... > Black Heads and Tails**

## Notes

- Uses `flame.execute_shortcut("Overwrite Edit")` — the keyboard shortcut for Overwrite Edit must be active.
- After running, the playhead is moved to the start, the timeline is framed, and focus is set to the top track.
