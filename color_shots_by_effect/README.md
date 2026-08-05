# Color Shots by Effect

**Script:** `color_shots_by_effect.py`  
**Version:** 1.0 | **Flame:** 2021.1+  
**Context:** Media Panel (right-click on sequence)

## Description

Generalized version of [Color Timewarp Shots](../color_timewarp_shots/): instead of only Timewarps, it colors segments containing **any** chosen timeline effect (Action, Image, Blur, Timewarp, etc.).

The script scans the selected sequences and lists the timeline effect types actually present — each with a count of how many segments carry it. Pick an effect and a color (nine presets, or **Custom...** for a full color picker) and every segment containing that effect is colored. Gives a quick visual overview of effected shots during conform or finishing.

## Usage

1. Select one or more sequences in the Media Panel.
2. Right-click → **Sequence... > Color Shots by Effect**
3. Choose a timeline effect and a color, then **OK**.

Run it again with a different effect/color combination to build up a color-coded overview.

## Requirements

- Flame 2021+
- Selection must contain `PySequence` objects
