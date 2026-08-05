# Surround Sound Mute / Unmute

**Script:** `surround_sound_mute_unmute.py`  
**Version:** 1.0 | **Flame:** 2020+  
**Context:** Media Panel (right-click on clip)  
**Original by:** John Geehreng | **Combined by:** Bryan Bayley

## Description

Mutes or unmutes the first 6 audio tracks on selected clips/sequences. This targets a standard 5.1 surround sound layout (tracks 1–6).

## Actions

| Action | Description |
|--------|-------------|
| **Mute Surround Channels** | Sets `mute = True` on audio tracks 0–5 |
| **Unmute Surround Channels** | Sets `mute = False` on audio tracks 0–5 |

## Usage

1. Select one or more clips in the Media Panel.
2. Right-click → **Audio... > Mute Surround Channels** or **Unmute Surround Channels**

## Requirements

- Flame 2020+
- Clips with fewer than 6 audio tracks are handled gracefully — only the tracks that exist are toggled
- Selection must contain `PyClip` objects
