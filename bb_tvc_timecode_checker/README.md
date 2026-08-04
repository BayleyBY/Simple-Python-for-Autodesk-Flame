# BB TVC Timecode Checker

**Script:** `bb_tvc_timecode_checker.py`  
**Version:** 2.1 | **Flame:** 2026.1  
**Context:** Media Panel (right-click on clips or sequences)

## Description

Checks selected clips or sequences against broadcast TVC delivery specs:

1. Does the record timecode start at `01:00:00:00` — or at a recognized lead-in start?
   - `59:59:00` → assumed 1s of black at head and tail (total = program + 2s)
   - `59:50:00` / `59:53:00` → assumed 10s / 7s slate lead-in, nothing after the program
   For sequences whose container start matches none of these, the first segment's record-in is checked as a fallback.
2. Is the duration a standard TVC length (6s, 15s, 30s, 60s, 90s) after accounting for the assumed layout? Durations are measured against the integer timebase (23.976 → 24), so a 720-frame spot counts as 30s. Non-standard whole-second lengths and odd (partial-second) durations are reported separately.

The results dialog is condensed: when everything passes it reports one line per layout (e.g. "All 4 timelines have 1s black head + tail and are the correct length"), and since layouts are inferred from the start timecode only — the script can't see whether a slate or black is really there — it asks for a visual confirm whenever a layout was assumed. Per-item detail appears only for failures and errors; the shell always logs every item.

## Menus

- Right-click on clips or sequences in the Media Panel → TVC Checks... → Check Start Timecode and Duration
