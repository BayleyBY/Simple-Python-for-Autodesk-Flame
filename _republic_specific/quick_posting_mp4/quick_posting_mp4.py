"""
Script Name: Quick Posting MP4
Script Version: 1.0
Flame Version: 2024
Written by: Bryan Bayley
Creation Date: 05.05.23

Description:
Export selected clips to the job folder / Postings folder. Creates a new dated
folder, rounding the minutes to the nearest 15-minute increment. After export,
remuxes the .mov to .mp4 using ffmpeg and copies a shortened path to the
clipboard for Slack sharing.

Menus:
Right-click a clip in the Media Panel -> Export... -> Quick Posting MP4

Requirements:
- Facilis partitions must be mounted at /Volumes.
- Flame Project Nickname must be the Facilis partition name (e.g. Republic_2023_Q1).
- Flame Project Name must match the job folder (e.g. R2305590_Client_Project).
- ffmpeg at /usr/local/bin/ffmpeg.
- Export preset: /opt/Autodesk/shared/export/presets/movie_file/Quick_Posting_MP4.xml.
"""

import datetime
import os
import subprocess
import flame

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

# Shared state between export_clips and the post_export_sequence hook.
_export_path = None
_export_filename = None


def export_clips(selection):
    global _export_path, _export_filename

    def resolve_path(clip, template):
        date = datetime.datetime.now()
        approx = round(date.minute / 15.0) * 15
        date = date.replace(minute=0) + datetime.timedelta(seconds=approx * 60)
        time_part = date.time()
        path = template
        path = path.replace("<ProjectName>", str(flame.project.current_project.name)[1:-1])
        path = path.replace("<ProjectNickName>", str(flame.project.current_project.nickname)[1:-1])
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
        _export_path = resolve_path(clip, template)
        _export_filename = str(clip.name)[1:-1] + ".mov"

        if not os.path.isdir(_export_path):
            os.makedirs(_export_path)

        clip_output.export(
            clip,
            "/opt/Autodesk/shared/export/presets/movie_file/Quick_Posting_MP4.xml",
            _export_path
        )

        flame.go_to("MediaHub")
        flame.mediahub.files.set_path(_export_path)

        # Build shortened path for Slack (strip /Volumes/<mount>/<job>/)
        folders = _export_path.split("/")
        slack_path = "/".join(folders[4:]).rstrip("/")
        QtWidgets.QApplication.instance().clipboard().setText(slack_path)


def scope_clip(selection):
    for item in selection:
        if isinstance(item, flame.PyClip):
            return True
    return False


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": "Export...",
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


def post_export_sequence(info, userData, *args, **kwargs):
    global _export_path, _export_filename

    if _export_path is None or _export_filename is None:
        return

    remux_source = os.path.join(_export_path, _export_filename)
    remux_dest = os.path.join(_export_path, os.path.splitext(_export_filename)[0] + ".mp4")

    ffmpeg_cmd = [
        "/usr/local/bin/ffmpeg", "-y", "-i", remux_source,
        "-codec:v", "copy", "-codec:a", "aac", "-ab", "320k", remux_dest
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    if os.path.isfile(remux_dest) and os.path.getsize(remux_dest) > 0:
        os.remove(remux_source)
        print("======= MP4 created successfully and MOV was deleted. =======")
    else:
        print("======= MP4 REMUX DID NOT COMPLETE =======")

    _export_path = None
    _export_filename = None
