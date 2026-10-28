"""
Script Name: Quick Posting Aspect Ratios
Script Version: 1.1
Flame Version: 2024
Written by: Bryan Bayley
Creation Date: 02.19.26
Update Date: 10.28.26

Description:
Export selected clips using a preset chosen by the clip name's trailing
aspect-ratio suffix. Uses the same dated output folder (rounded to the nearest
15 minutes) as Quick Posting MP4. After export, navigates MediaHub to the
folder, copies a shortened path to the clipboard, and opens a Finder window
there.

Suffix -> preset mapping:
    1x1  -> Posting_16x9_to_1x1.xml
    9x16 -> Posting_16x9_to_9x16.xml
    4x5  -> Posting_16x9_to_4x5.xml

Clips whose names don't end with a recognized suffix are skipped with a console
warning.

Menus:
Right-click clips in the Media Panel -> Export... -> Quick Posting — Social Aspect Ratios

Requirements:
- Facilis partitions mounted at /Volumes
- Flame Project Nickname must be the Facilis partition name (e.g. Republic_2023_Q1)
- Flame Project Name must match the job folder (e.g. R2305590_Client_Project)
- Aspect-ratio export presets present in PRESET_DIR (see CONFIG below)

Updates:

v1.1 10.28.26
- The Finder window no longer fails to open after a successful export.
  flame.execute_command() ran /usr/bin/open outside Flame's GUI session, so
  LaunchServices could not reach Finder and returned "procNotFound" (-600).
  Running open as a direct subprocess of Flame keeps it in the session.
  Same fix as Quick Posting MP4 v1.1.
- A failure to open Finder is now reported in the shell instead of raising,
  so the export itself is never lost to it.
"""

import datetime
import os
import subprocess
import flame

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

SCRIPT_NAME = "Quick Posting Aspect Ratios"
FOLDER = "Export..."


PRESET_DIR = "/Volumes/Flame_Archive/SHARED/export/presets/movie_file"

PRESET_MAP = {
    "1x1":  "Posting_16x9_to_1x1.xml",
    "9x16": "Posting_16x9_to_9x16.xml",
    "4x5":  "Posting_16x9_to_4x5.xml",
}


def get_dated_export_path():
    date = datetime.datetime.now()
    approx = round(date.minute / 15.0) * 15
    date = date.replace(minute=0)
    date += datetime.timedelta(seconds=approx * 60)

    path = "/Volumes/<ProjectNickName>/<ProjectName>/03_Exports/01_Postings/02_Online/<YY>-<MM>-<DD>-<Hour><Minute>/"
    path = path.replace("<ProjectName>", str(flame.project.current_project.name))
    path = path.replace("<ProjectNickName>", str(flame.project.current_project.nickname))
    path = path.replace("<YY>", date.strftime("%y"))
    path = path.replace("<MM>", date.strftime("%m"))
    path = path.replace("<DD>", date.strftime("%d"))
    path = path.replace("<Hour>", date.strftime("%H"))
    path = path.replace("<Minute>", date.strftime("%M"))

    return path


def get_preset_for_clip(clip_name):
    for suffix, preset_file in PRESET_MAP.items():
        if clip_name.endswith(suffix):
            return os.path.join(PRESET_DIR, preset_file)
    return None


def export_clips(selection):
    export_path = get_dated_export_path()

    if not os.path.isdir(export_path):
        os.makedirs(export_path, exist_ok=True)

    clip_output = flame.PyExporter()
    clip_output.use_top_video_track = True
    clip_output.foreground = True
    clip_output.export_between_marks = True

    skipped = []
    exported = []

    for clip in selection:
        if not isinstance(clip, flame.PyClip):
            continue

        clip_name = str(clip.name)[1:-1]
        preset_path = get_preset_for_clip(clip_name)

        if preset_path is None:
            flame.messages.show_in_console(
                f"Quick Posting (Aspect Ratio): Skipping '{clip_name}' — "
                f"name does not end with a recognized suffix ({', '.join(PRESET_MAP.keys())}).",
                "warning"
            )
            skipped.append(clip_name)
            continue

        clip_output.export(clip, preset_path, export_path)
        exported.append(clip_name)

    if exported:
        flame.go_to("MediaHub")
        flame.mediahub.files.set_path(export_path)

        # Build shortened path (everything after /Volumes/<mount>/<job>/)
        folders = export_path.split("/")
        slack_path = "/".join(folders[4:])
        slack_path = slack_path.rsplit("/", 1)[0]

        qt_app_instance = QtWidgets.QApplication.instance()
        qt_app_instance.clipboard().setText(slack_path)

        # Open a Finder window at the export folder.
        # Must be a direct subprocess of Flame, not flame.execute_command():
        # that runs open outside Flame's GUI session, where LaunchServices
        # cannot reach Finder and fails with "procNotFound" (-600). Passing the
        # path as a list element also removes the need to quote it for a shell.
        result = subprocess.run(
            ["/usr/bin/open", export_path], capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"[NOTE] could not open a Finder window at {export_path}")
            print(result.stderr.strip())

    if skipped:
        flame.messages.show_in_console(
            f"Quick Posting (Aspect Ratio): Skipped {len(skipped)} clip(s) with "
            f"unrecognized suffixes: {', '.join(skipped)}",
            "warning"
        )


def scope_clip(selection):
    for item in selection:
        if isinstance(item, flame.PyClip):
            return True
    return False


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": FOLDER,
            "actions": [
                {
                    "name": "Quick Posting — Social Aspect Ratios",
                    "isVisible": scope_clip,
                    "execute": export_clips,
                    "minimumVersion": "2022",
                }
            ]
        }
    ]
