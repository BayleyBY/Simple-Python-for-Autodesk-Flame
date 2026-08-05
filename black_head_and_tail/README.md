# Black Head and Tail

**Script:** `black_head_and_tail.py`  
**Version:** 1.1 | **Flame:** 2027  
**Context:** Media Panel (right-click on sequence)

## Description

Adds one second of virtual black to both the head and tail of selected sequences.

The black source is generated automatically — a temporary 1-second black Colour Source is created, used for the edits, and deleted afterward — so nothing needs to be set up on the desktop beforehand. The head black is placed before the first frame and the tail black after the last frame; neither edit ripples or shifts existing content, and each black handle's timeline segment colour is set to black.

## Prerequisites

- Set each sequence's **record patch** to the track you want the black on before running (the patch cannot be controlled from Python).

## Usage

1. Select one or more sequences in the Media Panel.
2. Set track patching on each sequence.
3. Right-click → **Conform... > Black Heads and Tails**

## Notes

- Works on a batch of sequences. Each is isolated so one failure can't abort the rest, and a warning dialog lists any sequence whose head or tail was not added (e.g. a sequence with no room before its start). Per-sequence results are also printed to the console.
- After running, the original selection and active timeline are restored.
- Uses `flame.execute_shortcut("Overwrite Edit")` — the Overwrite Edit shortcut must be active.
