# Create Marker with Segment Duration

**Script:** `_BB_create_marker_001.py`  
**Version:** 1.0 | **Flame:** 2021.1+  
**Context:** Timeline (right-click on segment)

## Description

Creates a marker that spans the exact duration of the selected segment. Two options are available:

| Action | Description |
|--------|-------------|
| **Create Marker on Segment Duration** | Creates a clip-level marker at the segment's record in-point, spanning the segment's duration |
| **Create Segment Marker on Segment Duration** | Creates a segment-level marker directly on the segment, spanning its duration |

Useful for quickly marking a region of interest that corresponds precisely to an edit point or segment boundary.

## Usage

1. In the Timeline, right-click on a segment.
2. Select **MARKERS... > Create Marker on Segment Duration** or **Create Segment Marker on Segment Duration**

## Requirements

- Selection must contain `PySegment` objects
