"""
Script Name: Insert Slate
Script Version: 1.0
Flame Version: 2027
Written by: Bryan Bayley
Creation Date: 08.05.26

Description:
Inserts a slate clip at the head of one or more sequences, starting at
00:59:53:00 on a new top video track. Select the slate clip together with
the target sequence(s) in the Media Panel: the one selected item that is
not a sequence is taken as the slate. If a sequence starts after
00:59:53:00 (e.g. at 01:00:00:00 or 00:59:59:00), its head is first
extended with virtual padding so the slate position exists, then the
playhead is parked at 00:59:53:00 and the slate is overwritten onto the
topmost existing video track at that spot. Nothing ripples - the existing
content keeps its timecode.

Prerequisites:
- This script uses flame.execute_shortcut(). The shortcuts used must still
  exist in the Keyboard Shortcut editor (they do by default): Overwrite
  Edit, Timeline Home, Set Focus on Topmost Visible Track.

Menus:
Right-click a slate clip and sequence(s) in the Media Panel -> Sequence... -> Insert Slate at 00:59:53:00
"""

import re
import traceback

import flame

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

SCRIPT_NAME = "Insert Slate"

# Absolute record timecode where the slate starts.
SLATE_TIMECODE = "00:59:53:00"


def message_box(message):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle(SCRIPT_NAME)
    msg.setText(message)
    msg.exec()


def scope_clip(selection):
    for item in selection:
        if isinstance(item, flame.PyClip):
            return True
    return False


def timecode_fields(value):
    """(hours, minutes, seconds, frames) ints from a PyTime (possibly
    wrapped in a PyAttribute) - str(PyTime) renders quoted with '+' (or
    ';' for drop-frame) before the frames field, e.g. '00:59:58+00'."""
    if hasattr(value, "get_value"):
        value = value.get_value()
    match = re.search(r"(\d+)[:;+.](\d{2})[:;+.](\d{2})[:;+.](\d{2,3})", str(value))
    if match is None:
        raise ValueError("could not parse timecode from %s" % str(value))
    return tuple(int(field) for field in match.groups())


def fields_to_frames(fields, one_second):
    hours, minutes, seconds, frames = fields
    return ((hours * 60 + minutes) * 60 + seconds) * one_second + frames


def insert_slate_in_sequence(clip, slate):
    # Make sure the clip is open as a sequence
    clip.open()

    # Sequence timing: one second of frames at the sequence's own rate and
    # its start timecode. start_time is a PyAttribute - unwrap it.
    seq_start = clip.start_time.get_value()
    one_second = round(float(str(clip.frame_rate).split()[0]))
    target = flame.PyTime(SLATE_TIMECODE, clip.frame_rate)

    # Extend the head with virtual padding when the sequence starts after
    # the slate position, so 00:59:53:00 exists on the timeline.
    # padding_start needs an absolute timecode PyTime. Compare positions by
    # parsed timecode fields - .frame numbers from different PyTime sources
    # live in different spaces.
    start_fields = timecode_fields(seq_start)
    target_fields = timecode_fields(target)
    if target_fields < start_fields:
        clip.padding_start = target

    # A slate longer than the gap runs past the original sequence start -
    # on the existing top track that means overwriting picture. Insert it
    # anyway, but say so in the shell.
    gap_frames = (fields_to_frames(start_fields, one_second)
                  - fields_to_frames(target_fields, one_second))
    slate_frames = int(slate.duration.frame)
    if gap_frames > 0 and slate_frames > gap_frames:
        print("%s: NOTE - slate is %d frames but only %d frames before the "
              "original start; it will overwrite picture on the top track "
              "from %s"
              % (SCRIPT_NAME, slate_frames, gap_frames,
                 str(seq_start).strip("'")))

    # Overwrite the slate at the playhead on the existing top track: clear
    # any in/out marks so they cannot steer the edit, make the top track
    # primary (Overwrite Edit follows the primary track), park the playhead
    # at the slate timecode and Overwrite Edit with the slate selected in
    # the Media Panel. The topmost track is the last track of the LAST
    # version - versions[0] is the bottom version, so on a multi-version
    # sequence versions[0].tracks[-1] points mid-stack and flips the
    # primary/secondary assignment.
    clip.in_mark = None
    clip.out_mark = None
    clip.primary_track = clip.versions[-1].tracks[-1]
    clip.current_time = target
    flame.media_panel.selected_entries = [slate]
    flame.execute_shortcut("Overwrite Edit")

    # Move the playhead to the start of the sequence (frame 1 = the slate
    # start now that the head is padded), frame the whole timeline, and put
    # the edit focus back on the top track where the slate is - Overwrite
    # Edit moves it to the secondary track as a side effect.
    clip.current_time = flame.PyTime(1)
    flame.execute_shortcut("Timeline Home")
    flame.execute_shortcut("Set Focus on Topmost Visible Track")


def insert_slate(selection):
    slates = []
    sequences = []
    for item in selection:
        if isinstance(item, flame.PySequence):
            sequences.append(item)
        elif isinstance(item, flame.PyClip):
            slates.append(item)

    if len(slates) != 1 or not sequences:
        message_box(
            "Select one slate clip together with the sequence(s) to slate."
            "\n\nSelected: %d clip(s), %d sequence(s)."
            % (len(slates), len(sequences)))
        return

    slate = slates[0]
    failed = []

    for clip in sequences:
        clip_name = str(clip.name)[1:-1]
        print("%s: ----- '%s' -----" % (SCRIPT_NAME, clip_name))
        try:
            insert_slate_in_sequence(clip, slate)
            print("%s: slate inserted at %s in '%s'"
                  % (SCRIPT_NAME, SLATE_TIMECODE, clip_name))
        except Exception:
            print("%s: ERROR while slating '%s':" % (SCRIPT_NAME, clip_name))
            traceback.print_exc()
            failed.append(clip_name)

    flame.media_panel.selected_entries = sequences

    if failed:
        message_box(
            "An error interrupted the slate insert on:\n\n"
            + "\n".join(failed)
            + "\n\nSee the Flame shell for details.")


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": "Sequence...",
            "actions": [
                {
                    "name": "Insert Slate at 00:59:53:00",
                    "isVisible": scope_clip,
                    "execute": insert_slate
                }
            ]
        }
    ]
