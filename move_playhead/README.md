# Move Playhead

**Script:** `move_playhead.py`  
**Version:** 2.0 | **Flame:** 2025+  
**Context:** Media Panel (right-click on clips or sequences)

## Description

Moves the playhead (positioner) of all selected clips or sequences to an absolute record timecode.

The timecodes in the menu are **yours to set**. **Setup...** opens a window where you add, label, reorder and remove as many timecodes as you need, and each one becomes its own action in the same menu. Settings are saved to `move_playhead_config.json` next to the script, so the menu comes back the same way in every project.

Out of the box the menu offers `00:59:53:00` and `01:00:00:00` plus a custom-timecode dialog — the same as version 1.0. Nothing changes until you edit it.

The playhead can be parked **before the first frame** of the sequence (verified in Flame 2027.1): setting `00:59:53:00` on a sequence whose record starts at `01:00:00:00` (or `00:59:59:00`) lands exactly on target, with no clamping. This is useful for preparing slate insertions and other head work at standard broadcast lead-in positions across many sequences at once.

## Usage

1. Select one or more clips or sequences in the Media Panel.
2. Right-click → **Move Playhead...** → pick one of your timecodes (or **Move Playhead to Custom Timecode** to type a one-off as `HH:MM:SS:FF`).

Each clip's playhead moves to the chosen timecode. Failures (if any) are listed in a dialog at the end; the run continues past them.

## Setting up your own timecodes

Right-click → **Move Playhead... > Setup...**

- **Add Timecode** adds a row. Enter the timecode as `HH:MM:SS:FF` — use a semicolon before the frames (`00:59:52;00`) for drop frame.
- The **Label** is optional. With one, the menu reads `Move Playhead to Slate (00:59:53:00)`; without one, just `Move Playhead to 00:59:53:00`.
- **▲ / ▼** reorder the rows — the menu follows this order.
- **✕** removes a row.
- The **Custom Timecode** action can be switched off if you never use it.

Settings are saved next to the script as `move_playhead_config.json` (falling back to `~/.move_playhead_config.json` when the script folder is not writable). After saving, the script asks Flame to rescan its Python hooks so the new menu appears right away; if that does not happen, use **Flame menu → Rescan Python Hooks**.

## Requirements

- Flame 2025+ (PySide6, with PySide2 fallback for older versions)
- Selection must contain `PyClip` objects (clips or sequences)
- The script folder should be writable if you want the settings shared with everyone loading the script (otherwise they are saved per user in the home directory)
