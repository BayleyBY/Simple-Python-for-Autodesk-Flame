"""
Script Name: Set In Out
Script Version: 1.1
Flame Version: 2021.1
Written by: Bryan Bayley
Creation Date: 07.29.21
Updated: 08.04.26

Description:
Set In/Out marks on selected clips for common delivery and approval workflows.
All presets assume:
- 23.98/24 fps
- Slate at 59:53:00
- First frame of picture at 1:00:00:00
- 1 second black at end of sequence

Menus:
Right-click a clip in the Media Panel -> Set In-Out... -> Clear All In-Out
Right-click a clip in the Media Panel -> Set In-Out... -> One Second Heads and Tails
Right-click a clip in the Media Panel -> Set In-Out... -> Slated with Tails
Right-click a clip in the Media Panel -> Set In-Out... -> Slated no Tails
Right-click a clip in the Media Panel -> Set In-Out... -> Frame-to-Frame
"""

import flame

SCRIPT_NAME = "Set In Out"
FOLDER = "Set In-Out..."


def clear_in_out(selection):
    for clip in selection:
        clip.in_mark = None
        clip.out_mark = None


def in_out_posting(selection):
    for clip in selection:
        clip.in_mark = None
        clip.out_mark = None
        clip.out_mark = int(clip.duration.frame) + 1
        clip.in_mark = flame.PyTime("00:59:59:00", clip.frame_rate)


def in_out_slated_approval(selection):
    for clip in selection:
        clip.in_mark = None
        clip.out_mark = None
        clip.out_mark = int(clip.duration.frame) + 1
        clip.in_mark = flame.PyTime("00:59:53:00", clip.frame_rate)


def in_out_slated(selection):
    for clip in selection:
        clip.in_mark = None
        clip.out_mark = None
        clip.out_mark = int(clip.duration.frame) - 23
        clip.in_mark = flame.PyTime("00:59:53:00", clip.frame_rate)


def in_out_olv(selection):
    for clip in selection:
        clip.in_mark = None
        clip.out_mark = None
        clip.out_mark = int(clip.duration.frame) - 23
        clip.in_mark = flame.PyTime("01:00:00:00", clip.frame_rate)


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
                    "name": "Clear All In-Out",
                    "isVisible": scope_clip,
                    "execute": clear_in_out,
                    "minimumVersion": "2022"
                },
                {
                    "name": "One Second Heads and Tails",
                    "isVisible": scope_clip,
                    "execute": in_out_posting,
                    "minimumVersion": "2022"
                },
                {
                    "name": "Slated with Tails",
                    "isVisible": scope_clip,
                    "execute": in_out_slated_approval,
                    "minimumVersion": "2022"
                },
                {
                    "name": "Slated no Tails",
                    "isVisible": scope_clip,
                    "execute": in_out_slated,
                    "minimumVersion": "2022"
                },
                {
                    "name": "Frame-to-Frame",
                    "isVisible": scope_clip,
                    "execute": in_out_olv,
                    "minimumVersion": "2022"
                }
            ]
        }
    ]
