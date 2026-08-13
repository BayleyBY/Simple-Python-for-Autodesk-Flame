# Add View Transform Track

**Script:** `add_view_transform_track.py`  
**Version:** 1.0 | **Flame:** 2027+  
**Context:** Media Panel (right-click on sequence)

## Description

Adds a new video track to the selected sequences and puts a Colour Management gap effect on it, switched from its default **Colour Transform** mode to **View Transform**.

This gives a sequence a display transform sitting over the picture below it without touching any of the existing segments — the effect lives on the new track's gap, so nothing on the original tracks is modified.

## Track Placement

The new track goes directly **below the topmost track**, which puts the view transform between the footage and the graphics sitting above it.

This is measured per sequence, from that sequence's own track count, so a selection mixing three-, four- and five-track sequences still lands the new track second from the top in every one of them. Nothing about the placement depends on the playhead or on which sequence is open in the timeline.

The track is inserted with `create_track(len(tracks))`, since positive track indices are 1-based (`-1` appends on top, `0` raises *Invalid track index*): landing above the track at 0-based position *i* means inserting at *i* + 2, and the track below the topmost one is at `len(tracks) - 2`.

A **single-track** sequence has nothing to sit below, so its new track is added on top. The Flame shell prints which of the two paths was taken for each sequence.

For multi-version sequences the track is added to the topmost version (`versions[-1]`). Single-version sequences — the normal case — are unaffected by this.

## Limitation — one graphics track

The script has no way to tell graphics from footage, so it treats **the topmost track as the graphics track** and slides the new track in underneath it.

That is only correct when the graphics are on a **single** track at the time the script is run. A sequence carrying two or more graphics tracks gets the view transform inserted *between* them — the lower graphics track ends up under the transform along with the footage.

Two ways around it:

- run the script while the graphics are still on one track, then build the extra graphics tracks above the new one
- move the new track down by hand afterwards

The script does not detect the situation or warn about it.

## Picture Range

The effect covers the picture only — black heads and tails are left uncovered.

Before the track is added, the existing tracks are scanned for the first and last **picture** segment, and the new track's gap is then cut down to that range with `track.cut(cut_time=…)`. The effect goes on the middle piece.

A segment is not picture when either:

- its `type` is `"Gap"`, or
- it has an empty `file_path` — a black head or tail is a colour source, which carries no media

A slate is real picture, so it falls **inside** the covered range.

If no picture is found, or the range can't be isolated, the effect covers the whole track and the Flame shell says so.

## Effect Settings

Only the mode is set. Tagged Colour Space, View and Display are left at Flame's defaults, so the effect follows the project's colour management settings.

The effect type is `Colour Mgmt` — the gap/segment flavour. `Source Colour Mgmt` is a separate source-side effect and is not what a gap takes.

## Usage

1. Select one or more sequences in the Media Panel.
2. Right-click → **Sequence... > Add View Transform Track**

Running the script twice stacks a second View Transform track — there is no duplicate check.

## Requirements

- Flame 2027+
- PySide6 (or PySide2 on Flame before 2025) for the error dialog
- Selection must contain `PySequence` objects

## Notes

Sequences are handled one at a time: a failure on one is reported to the Flame shell and the remaining sequences still run, with a summary dialog at the end listing anything that was skipped.
