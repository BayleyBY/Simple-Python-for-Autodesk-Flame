# Select Connected in Media Panel

**Script:** `select_connected_in_media_panel.py`  
**Version:** 1.0 | **Flame:** 2026.2+  
**Context:** Timeline (right-click on a segment)  
**Based on:** Fred Warren's script

## Description

Adds a **Connected Segments...** menu to the Timeline that traces the Media Panel clips connected to the focused timeline segment.

## Actions

| Action | Description |
|--------|-------------|
| **Select Connected Clips in Media Panel** | Finds all clips containing segments connected to the focused segment, expands their parent reels, and selects them. |
| **Select and Color Clips in Media Panel** | Same as above, and also colours each connected clip green for visual identification — handy when the clips span multiple reels. |
| **Uncolor Connected Clips** | Removes the green colour from the connected clips. |

The actions only appear when the focused segment has 2 or more connected segments. Operates on the single focused segment (no multi-segment selection).

## Usage

1. In the Timeline, right-click the segment you want to trace.
2. Right-click → **Connected Segments... > [action]**

## Requirements

- Flame 2023+
