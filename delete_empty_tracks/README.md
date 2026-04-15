# Delete Empty Tracks

**Script:** `_BB_delete_empty_tracks_001.py`  
**Version:** 1.0 | **Flame:** 2022.1+  
**Context:** Media Panel (right-click on sequence)

## Description

Deletes all empty video and audio tracks from selected sequences. A track is considered empty if it contains only a single Gap segment.

Handles stereo track pairs correctly — when a stereo track is found, both channels are evaluated together and neither is deleted unless both are empty.

## What Gets Deleted

- **Video tracks** — any track containing only a Gap segment
- **Audio channels** — any channel containing only a Gap segment (stereo pairs respected)

## Usage

1. Select one or more sequences in the Media Panel.
2. Right-click → **Sequence... > Delete All Empty Tracks**

## Requirements

- Flame 2021.1+
- Selection must contain `PySequence` objects
