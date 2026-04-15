# Open PSD in Photoshop

**Script:** `_BB_open_photoshop_007.py`  
**Version:** 1.0 | **Flame:** 2024+  
**Context:** Timeline / Batch / Media Panel / MediaHub  
**Help from:** Michael Vaglienty

## Description

Opens the source PSD file of a soft-imported clip in Photoshop (or whatever app is set as the default for `.psd` files on macOS). Works across all four Flame panels.

The script uses `subprocess.call(('open', clip_path))` which delegates to macOS's `open` command — Photoshop must be the default application for `.psd` files.

## Supported Panels

| Panel | Right-click menu |
|-------|-----------------|
| Timeline | Open... > Open PSD in Photoshop |
| Batch | Open... > Open PSD in Photoshop |
| Media Panel | Open... > Open PSD in Photoshop |
| MediaHub | Open... > Open PSD in Photoshop |

The context menu only appears when the selected item is a `.psd` file. To support additional extensions (`.jpg`, `.png`, etc.), add them to the `valid_extensions` list in `valid_file_extension()`.

## Files

| File | Description |
|------|-------------|
| `_BB_open_photoshop_007.py` | Current version |
| `_BB_open_photoshop_008.bak` | Work-in-progress backup of next version |

## Requirements

- macOS
- Flame 2023+
- Photoshop set as default app for `.psd` files
