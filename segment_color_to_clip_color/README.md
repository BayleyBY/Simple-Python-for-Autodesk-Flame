# Segment Color to Clip Color

**Script:** `segment_color_to_clip_color.py`  
**Version:** 1.0 | **Flame:** 2024.1+  
**Context:** Media Panel (right-click on clip)  
**Help from:** Fred Warren

## Description

Takes the colour label of the first segment in a clip and applies it at the clip level.

Useful in a color grading workflow with a timeline and source clips: colour labels applied to segments in the timeline sync to the sources at the segment level only. This copies the label up to the clip level, making it easier to see that sources are connected to the segments in the sequences.

## Usage

1. Select one or more clips in the Media Panel.
2. Right-click → **Sequence... > Copy Segment Color to Clip Color**

## Requirements

- Flame 2024+
- Selection must contain `PyClip` objects
