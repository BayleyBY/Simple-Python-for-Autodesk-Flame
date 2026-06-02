"""
Script Name: Open PSD in Photoshop
Script Version: 1.0
Flame Version: 2024
Written by: Bryan Bayley
Help from: Michael Vaglienty
Creation Date: 07.13.23

Description:
If a clip or timeline segment is a soft-imported PSD file, open the source file
in Photoshop. Written for macOS - Photoshop must be the default app for PSD
files.

Menus:
Right-click a clip in the Timeline -> Open... -> Open PSD in Photoshop
Right-click a Clip node in Batch -> Open... -> Open PSD in Photoshop
Right-click a clip in the Media Panel -> Open... -> Open PSD in Photoshop
Right-click a file in the MediaHub -> Open... -> Open PSD in Photoshop
"""

import os
import subprocess
import flame


def valid_file_extension(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower() in [".psd"]


def timeline_psd(selection):
    for item in selection:
        clip_path = item.file_path
        if clip_path and os.path.isfile(clip_path):
            subprocess.run(["open", clip_path])


def batch_psd(selection):
    for item in selection:
        clip_path = str(item.media_path)[1:-1]
        if clip_path and os.path.isfile(clip_path):
            subprocess.run(["open", clip_path])


def mediapanel_psd(selection):
    for item in selection:
        clip_path = item.versions[0].tracks[0].segments[0].file_path
        if clip_path and os.path.isfile(clip_path):
            subprocess.run(["open", clip_path])


def mediahub_psd(selection):
    for item in selection:
        if item.path is not None:
            subprocess.run(["open", item.path])


def scope_timeline_clip(selection):
    for item in selection:
        if isinstance(item, flame.PySegment) and item.file_path != "":
            if valid_file_extension(item.file_path):
                return True
    return False


def scope_batch_clip(selection):
    for item in selection:
        if item.type == "Clip":
            clip_path = str(item.media_path)[1:-1]
            if clip_path and valid_file_extension(clip_path):
                return True
    return False


def scope_clip(selection):
    for item in selection:
        if isinstance(item, flame.PyClip):
            clip_path = item.versions[0].tracks[0].segments[0].file_path
            if clip_path and valid_file_extension(clip_path):
                return True
    return False


def scope_file(selection):
    for item in selection:
        if valid_file_extension(str(item.path)):
            return True
    return False


def get_timeline_custom_ui_actions():
    return [
        {
            "name": "Open...",
            "actions": [
                {
                    "name": "Open PSD in Photoshop",
                    "isVisible": scope_timeline_clip,
                    "execute": timeline_psd,
                    "minimumVersion": "2023"
                }
            ]
        }
    ]


def get_batch_custom_ui_actions():
    return [
        {
            "name": "Open...",
            "actions": [
                {
                    "name": "Open PSD in Photoshop",
                    "isVisible": scope_batch_clip,
                    "execute": batch_psd,
                    "minimumVersion": "2023"
                }
            ]
        }
    ]


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": "Open...",
            "actions": [
                {
                    "name": "Open PSD in Photoshop",
                    "isVisible": scope_clip,
                    "execute": mediapanel_psd,
                    "minimumVersion": "2023"
                }
            ]
        }
    ]


def get_mediahub_files_custom_ui_actions():
    return [
        {
            "name": "Open...",
            "actions": [
                {
                    "name": "Open PSD in Photoshop",
                    "isVisible": scope_file,
                    "execute": mediahub_psd,
                    "minimumVersion": "2023"
                }
            ]
        }
    ]
