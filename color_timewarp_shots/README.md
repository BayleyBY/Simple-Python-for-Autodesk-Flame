# Color Timewarp Shots

**Script:** `_BB_color_timewarp_shots_001.py`  
**Version:** 1.0 | **Flame:** 2021.1+  
**Context:** Media Panel (right-click on sequence)

## Description

Scans all segments in the selected sequences and colors any segment that contains a **Timewarp** timeline effect dark red `(96, 12, 12)`.

This gives a quick visual overview of which shots in a timeline have been retimed, making it easier to identify and manage timewarped shots during conform or finishing.

## Usage

1. Select one or more sequences in the Media Panel.
2. Right-click → **Sequence... > Color Timewarped Shots**

## Requirements

- Flame 2020+
- Selection must contain `PySequence` objects
