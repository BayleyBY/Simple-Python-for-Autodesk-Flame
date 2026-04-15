# Surround Sound Channels Mute / Unmute

**Script:** `_BB_surround_sound_mute_and_unmute.py`  
**Version:** 1.0 | **Flame:** 2020+  
**Context:** Media Panel (right-click on clip)  
**Original by:** John Geehreng | **Combined by:** Bryan Bayley

## Description

Mutes or unmutes the first 6 audio tracks on selected clips/sequences. This targets a standard 5.1 surround sound layout (tracks 1–6).

## Actions

| Action | Description |
|--------|-------------|
| **Mute Surround Channels** | Sets `mute = True` on audio tracks 0–5 |
| **UnMute Surround Channels** | Sets `mute = False` on audio tracks 0–5 |

## Usage

1. Select one or more clips in the Media Panel.
2. Right-click → **Audio > Mute Surround Channels** or **UnMute Surround Channels**

## Requirements

- Flame 2020+
- Clip must have at least 6 audio tracks
- Selection must contain `PyClip` objects
