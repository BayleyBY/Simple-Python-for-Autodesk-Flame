"""
Script Name: Surround Sound Mute Unmute
Script Version: 1.0
Flame Version: 2020
Written by: John Geehreng
Mute and Unmute combined by: Bryan Bayley
Creation Date: 06.06.20

Description:
Mute or unmute audio tracks 1-6 (standard 5.1 surround layout) on all
selected clips/sequences.

Menus:
Right-click a clip in the Media Panel -> Audio -> Mute Surround Channels
Right-click a clip in the Media Panel -> Audio -> Unmute Surround Channels
"""

import flame

SCRIPT_NAME = "Surround Sound Mute Unmute"
FOLDER = "Audio..."

SURROUND_TRACK_COUNT = 6


def mute_channels(selection):
    for item in selection:
        for i in range(min(SURROUND_TRACK_COUNT, len(item.audio_tracks))):
            item.audio_tracks[i].mute = True


def unmute_channels(selection):
    for item in selection:
        for i in range(min(SURROUND_TRACK_COUNT, len(item.audio_tracks))):
            item.audio_tracks[i].mute = False


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
                    "name": "Mute Surround Channels",
                    "isVisible": scope_clip,
                    "execute": mute_channels,
                    "minimumVersion": "2020"
                },
                {
                    "name": "Unmute Surround Channels",
                    "isVisible": scope_clip,
                    "execute": unmute_channels,
                    "minimumVersion": "2020"
                }
            ]
        }
    ]
