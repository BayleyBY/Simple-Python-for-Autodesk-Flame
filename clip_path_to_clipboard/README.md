# Clip Path to Clipboard

**Script:** `_BB_clip_path_to_clipboard_for_slack_001.py`  
**Version:** 2.0 | **Flame:** 2024+  
**Context:** Media Panel / Timeline / Batch / MediaHub  
**Original by:** Michael Vaglienty | **Modified by:** Bryan Bayley

## Description

Copies the source file path of selected clips to the clipboard. A modified version of Michael Vaglienty's original script that strips the leading `/Volumes/<mount>/<project>` portion from paths, producing shorter links that are easier to share in Slack or other tools.

## Context Menu Entries

| Context | Menu | Action |
|---------|------|--------|
| Media Panel | File Path... | Copy Path to Clipboard |
| Timeline | File Path... | Copy Path to Clipboard |
| Batch | File Path... | Copy Path to Clipboard |
| MediaHub | File Path... | Copy Full Path to Clipboard |
| MediaHub | File Path... | Copy Short Path to Clipboard |

## Short Path Logic

The **Copy Short Path** option (MediaHub only) removes the first 4 path components (`/Volumes/<mount>/<project>/`) and strips the filename, leaving just the relative folder path for sharing.

## Requirements

- Flame 2021+
- PySide2 (bundled with Flame)
