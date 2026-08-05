# Move Playhead

**Script:** `move_playhead.py`  
**Version:** 1.0 | **Flame:** 2025+  
**Context:** Media Panel (right-click on clips or sequences)

## Description

Moves the playhead (positioner) of all selected clips or sequences to an absolute record timecode — either a preset (`00:59:53:00`, `01:00:00:00`) or a custom timecode entered in a dialog.

The playhead can be parked **before the first frame** of the sequence (verified in Flame 2027.1): setting `00:59:53:00` on a sequence whose record starts at `01:00:00:00` (or `00:59:59:00`) lands exactly on target, with no clamping. This is useful for preparing slate insertions and other head work at standard broadcast lead-in positions across many sequences at once.

## Usage

1. Select one or more clips or sequences in the Media Panel.
2. Right-click → **Move Playhead... > Move Playhead to 00:59:53:00** (or `01:00:00:00`, or **Custom Timecode** to type your own as `HH:MM:SS:FF`).

Each clip's playhead moves to the chosen timecode. Failures (if any) are listed in a dialog at the end; the run continues past them.

## Requirements

- Flame 2025+ (PySide6, with PySide2 fallback for older versions)
- Selection must contain `PyClip` objects (clips or sequences)
