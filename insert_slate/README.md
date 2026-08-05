# Insert Slate

**Script:** `insert_slate.py`  
**Version:** 1.0 | **Flame:** 2027+  
**Context:** Media Panel (right-click on a slate clip + sequences)

## Description

Inserts a slate clip at the head of one or more sequences, starting at `00:59:53:00` on the topmost existing video track.

If a sequence starts after `00:59:53:00` (e.g. at `01:00:00:00` or `00:59:59:00`), its head is first extended with virtual padding so the slate position exists on the timeline. The playhead is then parked at `00:59:53:00`, the top track is made the primary track, and the slate is overwritten at that spot. Nothing ripples — existing content keeps its timecode.

## Usage

1. In the Media Panel, select the slate clip **and** the sequence(s) to slate in one selection. The one selected item that is not a sequence is taken as the slate.
2. Right-click → **Sequence... > Insert Slate at 00:59:53:00**

The slate lands at `00:59:53:00` on each sequence's top track; afterwards the whole timeline is framed (Timeline Home) with the playhead on the first frame and focus on the top track. Failures are listed in a dialog at the end; the run continues past them. If the slate is longer than the gap before the original sequence start, it is inserted anyway and a note is printed in the shell (it will overwrite picture on the top track past the original start).

## Requirements

- Flame 2027+
- The **Overwrite Edit**, **Timeline Home** and **Set Focus on Topmost Visible Track** keyboard shortcuts must exist in the Keyboard Shortcut editor (they do by default)
- Selection must contain exactly one non-sequence clip (the slate) and at least one `PySequence`
