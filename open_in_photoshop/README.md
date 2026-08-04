# Open in Photoshop

**Script:** `open_in_photoshop.py`  
**Version:** 1.0 | **Flame:** 2024+  
**Context:** Timeline / Batch / Media Panel / MediaHub  
**Help from:** Michael Vaglienty

Replaces the older *Open PSD in Photoshop* script.

## Description

Opens the source file of a soft-imported still image in Photoshop. Photoshop is targeted by its bundle id (`com.adobe.Photoshop`), so it does **not** need to be the default app for the file type — Launch Services finds whichever Photoshop version is installed. If Photoshop isn't installed, the file opens in the default app as a fallback.

Supported formats: `.psd` `.psb` `.png` `.jpg` `.jpeg` `.tif` `.tiff` `.tga` `.bmp` `.gif`.

**Frame sequences**: in the Timeline and Media Panel, the frame the playhead is parked on opens (when the playhead is inside the segment/clip); otherwise — and in Batch/MediaHub, which have no playhead — the first frame opens. A source only counts as a sequence when its filename has a 4+ digit dot/underscore-delimited frame counter *and* several of the neighbouring frame files exist on disk, so versioned stills (`logo_v002.psd`) and short-numbered stills families (`board_01.jpg`) are never offset to the wrong file.

## Supported Panels

| Panel | Right-click menu |
|-------|-----------------|
| Timeline | Open... > Open in Photoshop |
| Batch | Open... > Open in Photoshop |
| Media Panel | Open... > Open in Photoshop |
| MediaHub | Open... > Open in Photoshop |

The context menu appears when any selected item is a supported still; in a mixed selection only the supported stills are opened. Missing source files (and any per-item errors) are reported in a single dialog at the end of the run. To support additional extensions, add them to the `EXTENSIONS` list.

## Requirements

- macOS
- Flame 2023+
- Photoshop (any version) — falls back to the default app if not installed
