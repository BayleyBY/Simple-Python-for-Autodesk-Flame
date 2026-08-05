"""
Script Name: Clip Path to Clipboard
Script Version: 1.0
Flame Version: 2024
Written by: Michael Vaglienty
Modified for shortened paths by: Bryan Bayley
Creation Date: 06.16.19

Description:
Copy a clip's source file path to the clipboard. Works in the Timeline, Media
Panel, Batch, and MediaHub. The MediaHub short-path option removes the leading
/Volumes/<mount>/<project> to shorten links when sharing via Slack.

Menus:
Right-click a clip in the Media Panel -> File Path... -> Copy Path to Clipboard
Right-click a clip in the Timeline -> File Path... -> Copy Path to Clipboard
Right-click a Clip node in Batch -> File Path... -> Copy Path to Clipboard
Right-click a file in the MediaHub -> File Path... -> Copy Full Path to Clipboard
Right-click a file in the MediaHub -> File Path... -> Copy Short Path to Clipboard
"""

import re
import flame

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

SCRIPT_NAME = "Clip Path to Clipboard"
FOLDER = "File Path..."


def _set_clipboard(text):
    QtWidgets.QApplication.instance().clipboard().setText(text)


def media_panel_copy_path(selection):
    paths = [
        clip.versions[0].tracks[0].segments[0].file_path.rsplit("/", 1)[0]
        for clip in selection
        if clip.versions[0].tracks[0].segments[0].file_path
    ]
    _set_clipboard("\n".join(paths))


def timeline_copy_path(selection):
    paths = [clip.file_path.rsplit("/", 1)[0] for clip in selection if clip.file_path]
    _set_clipboard("\n".join(paths))


def batch_copy_path(selection):
    paths = [
        str(clip.media_path)[1:-1].rsplit("/", 1)[0]
        for clip in selection
        if str(clip.media_path)[1:-1]
    ]
    _set_clipboard("\n".join(paths))


def mediahub_copy_path(selection):
    clip = selection[0]
    clip_path = clip.path.rsplit("/", 1)[0]
    if clip_path:
        _set_clipboard(clip_path)


def mediahub_copy_shortpath(selection):
    clip = selection[0]
    clip_path = clip.path
    if clip_path:
        # Remove /Volumes/<mount>/<job name>/
        folders = clip_path.split("/")
        slack_path = "/".join(folders[4:]).rsplit("/", 1)[0]
        _set_clipboard(slack_path)


def scope_timeline_clip(selection):
    for item in selection:
        if isinstance(item, flame.PySegment) and item.file_path != "":
            return True
    return False


def scope_batch_clip(selection):
    for item in selection:
        if item.type == "Clip":
            clip_path = str(item.media_path)[1:-1].rsplit("/", 1)[0]
            if clip_path:
                return True
    return False


def scope_clip(selection):
    for item in selection:
        if isinstance(item, flame.PyClip):
            if item.versions[0].tracks[0].segments[0].file_path != "":
                return True
    return False


def scope_file(selection):
    for item in selection:
        item_path = str(item.path)
        if re.search(r"\.\w{3}$", item_path, re.I) is not None:
            return True
    return False


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": FOLDER,
            "actions": [
                {
                    "name": "Copy Path to Clipboard",
                    "isVisible": scope_clip,
                    "execute": media_panel_copy_path,
                    "minimumVersion": "2021"
                }
            ]
        }
    ]


def get_batch_custom_ui_actions():
    return [
        {
            "name": FOLDER,
            "actions": [
                {
                    "name": "Copy Path to Clipboard",
                    "isVisible": scope_batch_clip,
                    "execute": batch_copy_path,
                    "minimumVersion": "2021"
                }
            ]
        }
    ]


def get_mediahub_files_custom_ui_actions():
    return [
        {
            "name": FOLDER,
            "actions": [
                {
                    "name": "Copy Full Path to Clipboard",
                    "isVisible": scope_file,
                    "execute": mediahub_copy_path,
                    "minimumVersion": "2021"
                },
                {
                    "name": "Copy Short Path to Clipboard",
                    "isVisible": scope_file,
                    "execute": mediahub_copy_shortpath,
                    "minimumVersion": "2021"
                }
            ]
        }
    ]


def get_timeline_custom_ui_actions():
    return [
        {
            "name": FOLDER,
            "actions": [
                {
                    "name": "Copy Path to Clipboard",
                    "isVisible": scope_timeline_clip,
                    "execute": timeline_copy_path,
                    "minimumVersion": "2021"
                }
            ]
        }
    ]
