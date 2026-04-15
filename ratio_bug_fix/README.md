# Ratio Bug Fix

**Script:** `_BB_ratio_bug_fix_001.py`  
**Version:** 1.0 | **Flame:** 2024.2+  
**Context:** Timeline (right-click on segment)

## Description

Workaround for a Flame bug where segments containing an **Action** timeline effect display the wrong size/ratio after conforming an AAF/XML with footage at a different resolution than the offline edit.

The fix works by adding a **Source Colour Mgmt** timeline effect to the segment and then immediately deleting it. This forces Flame to re-evaluate and correctly recognize the resolution of the source footage.

## Usage

1. In the Timeline, select the affected segment(s).
2. Right-click → **Segment... > Ratio Bug Fix**

## Requirements

- Flame 2020+
- Applies to timeline segments (`PySegment` objects)
