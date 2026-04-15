# Create Reel Group for Online Assemble

**Script:** `_BB_create_reel_group_002.py`  
**Version:** 1.0 | **Flame:** 2021.1+  
**Context:** Media Panel (right-click on Library)

## Description

Creates a standardized **Online Assemble** reel group inside the selected library, pre-configured with the reels and colors used for online finishing/conform work.

The reel group structure created:

| Reel | Type | Color |
|------|------|-------|
| `_Sources Sequence` | Sequence Reel | Black `(0, 0, 0)` |
| `Sources` | Standard Reel | Green `(29, 67, 45)` |
| `Conform` | Sequence Reel | Red `(96, 12, 12)` |

The reel group itself is colored dark red `(50, 0, 0)`. Any default "Reel" or "Sequences" reels added automatically by Flame are deleted.

## Usage

1. Right-click on a **Library** in the Media Panel.
2. Select **Create Reel Group > Create ReelGroup for Online Assemble**

## Related

See also `start_project` which calls this as part of a full project setup workflow.
