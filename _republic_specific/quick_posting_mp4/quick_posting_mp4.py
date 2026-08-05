"""
Script Name: Quick Posting MP4
Script Version: 1.0
Flame Version: 2024
Written by: Bryan Bayley
Creation Date: 05.05.23

Description:
Export selected clips to the job folder / Postings folder. Creates a new dated
folder, rounding the minutes to the nearest 15-minute increment, exports each
clip to MP4 with the posting preset, copies a shortened path to the clipboard
for Slack sharing, and opens a Finder window at the export folder.

Menus:
Right-click a clip in the Media Panel -> Export... -> Quick Posting MP4

Requirements:
- Facilis partitions must be mounted at /Volumes.
- Flame Project Nickname must be the Facilis partition name (e.g. Republic_2023_Q1).
- Flame Project Name must match the job folder (e.g. R2305590_Client_Project).
- Export preset: /Volumes/Flame_Archive/SHARED/export/presets/movie_file/ApprovalPosting_MP4_20Mbits.xml.
"""

import datetime
import os
import flame

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

SCRIPT_NAME = "Quick Posting MP4"
FOLDER = "Export..."


def export_clips(selection):

    def resolve_path(clip, template):
        date = datetime.datetime.now()
        approx = round(date.minute / 15.0) * 15
        date = date.replace(minute=0) + datetime.timedelta(seconds=approx * 60)
        time_part = date.time()
        path = template
        path = path.replace("<ProjectName>", str(flame.project.current_project.name))
        path = path.replace("<ProjectNickName>", str(flame.project.current_project.nickname))
        path = path.replace("<YYYY>", date.strftime("%Y"))
        path = path.replace("<YY>", date.strftime("%y"))
        path = path.replace("<MM>", date.strftime("%m"))
        path = path.replace("<DD>", date.strftime("%d"))
        path = path.replace("<Hour>", date.strftime("%H"))
        path = path.replace("<Minute>", time_part.strftime("%M"))
        path = path.replace("<AMPM>", date.strftime("%p"))
        return path

    template = (
        "/Volumes/<ProjectNickName>/<ProjectName>"
        "/03_Exports/01_Postings/02_Online/<YY>-<MM>-<DD>-<Hour><Minute>/"
    )

    clip_output = flame.PyExporter()
    clip_output.use_top_video_track = True
    clip_output.foreground = True
    clip_output.export_between_marks = True

    for clip in selection:
        export_path = resolve_path(clip, template)

        if not os.path.isdir(export_path):
            os.makedirs(export_path, exist_ok=True)

        clip_output.export(
            clip,
            "/Volumes/Flame_Archive/SHARED/export/presets/movie_file/ApprovalPosting_MP4_20Mbits.xml",
            export_path
        )

        flame.go_to("MediaHub")
        flame.mediahub.files.set_path(export_path)

        # Build shortened path for Slack (strip /Volumes/<mount>/<job>/)
        folders = export_path.split("/")
        slack_path = "/".join(folders[4:]).rstrip("/")
        QtWidgets.QApplication.instance().clipboard().setText(slack_path)

    # Open a Finder window at the export folder.
    # shell=True is required so the shell interprets the quotes around the path;
    # without it, execute_command passes the string to exec directly and the
    # quote characters become part of the path argument.
    if selection:
        flame.execute_command(f'/usr/bin/open "{export_path}"', shell=True)


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
                    "name": "Quick Posting MP4",
                    "isVisible": scope_clip,
                    "execute": export_clips,
                    "minimumVersion": "2022"
                }
            ]
        }
    ]
