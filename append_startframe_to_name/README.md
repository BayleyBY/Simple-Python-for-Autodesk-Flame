# Append Start Frame to Name

**Script:** `_BB_append_startframe_to_name_001.py`  
**Version:** 1.0 | **Flame:** 2023.1+  
**Context:** Media Panel (right-click on clip)

## Description

Appends the source start frame of a clip to the end of its name, zero-padded to 8 digits.

**Example:** `MyShot` → `MyShot_00086400`

This is useful when exporting multiple clips that share the same name. The start frame acts as a unique identifier to prevent files from overwriting each other — a workflow borrowed from color grading software like DaVinci Resolve for Color Pass exports.

## Usage

1. Select one or more clips in the Media Panel.
2. Right-click → **Rename... > Append Start Frame to Name**

## Requirements

- Flame 2020+
- Selection must contain `PyClip` objects
