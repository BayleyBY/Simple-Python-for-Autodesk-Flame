"""
Script Name: Move Playhead
Script Version: 1.0
Flame Version: 2025
Written by: Bryan Bayley
Creation Date: 08.05.26

Description:
Moves the playhead (positioner) of all selected clips or sequences to an
absolute record timecode — either a preset or a custom timecode entered in
a dialog. The playhead can be parked before the first frame of the
sequence (e.g. 00:59:53:00 on a sequence whose record starts at
01:00:00:00), which is useful for preparing slate insertions and other
head work at standard broadcast lead-in positions.

Menus:
Right-click selected clips or sequences in the Media Panel -> Move Playhead... -> Move Playhead to 00:59:53:00
Right-click selected clips or sequences in the Media Panel -> Move Playhead... -> Move Playhead to 01:00:00:00
Right-click selected clips or sequences in the Media Panel -> Move Playhead... -> Move Playhead to Custom Timecode
"""

import re
import traceback

import flame

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

TIMECODE_PATTERN = re.compile(r"^\d{1,2}:\d{2}:\d{2}[:;]\d{1,2}$")


def message_box(message):

    mbox = QtWidgets.QMessageBox()
    mbox.setWindowTitle("Move Playhead")
    mbox.setText(message)
    mbox.exec()


def move_playhead(selection, target_timecode):

    print("--- Move Playhead to %s ---" % target_timecode)
    failed = []

    for clip in selection:
        if not isinstance(clip, flame.PyClip):
            continue
        clip_name = str(clip.name)[1:-1]
        try:
            clip.current_time = flame.PyTime(target_timecode, clip.frame_rate)
            print("%s: playhead moved to %s" % (clip_name, target_timecode))
        except Exception:
            traceback.print_exc()
            failed.append(clip_name)

    if failed:
        message_box(
            "Could not move the playhead on:\n\n%s\n\nSee the shell for details."
            % "\n".join(failed))


def move_playhead_slate(selection):

    move_playhead(selection, "00:59:53:00")


def move_playhead_hour(selection):

    move_playhead(selection, "01:00:00:00")


def move_playhead_custom(selection):

    timecode, ok = QtWidgets.QInputDialog.getText(
        None, "Move Playhead", "Timecode (HH:MM:SS:FF):", text="01:00:00:00")
    if not ok:
        return

    timecode = timecode.strip()
    if not TIMECODE_PATTERN.match(timecode):
        message_box(
            "\"%s\" is not a valid timecode.\n\nUse HH:MM:SS:FF, e.g. 00:59:53:00."
            % timecode)
        return

    move_playhead(selection, timecode)


def scope_clip(selection):

    for item in selection:
        if isinstance(item, flame.PyClip):
            return True
    return False


def get_media_panel_custom_ui_actions():

    return [{
        "name": "Move Playhead...",
        "actions": [
            {
                "name": "Move Playhead to 00:59:53:00",
                "isVisible": scope_clip,
                "execute": move_playhead_slate
            },
            {
                "name": "Move Playhead to 01:00:00:00",
                "isVisible": scope_clip,
                "execute": move_playhead_hour
            },
            {
                "name": "Move Playhead to Custom Timecode",
                "isVisible": scope_clip,
                "execute": move_playhead_custom
            }
        ]
    }]
