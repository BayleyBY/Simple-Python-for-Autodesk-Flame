"""
Script Name: Delete Empty Tracks
Script Version: 1.0
Flame Version: 2022.1
Written by: Bryan Bayley
Creation Date: 08.11.21

Description:
Removes all empty video and audio tracks from selected sequences. Handles
stereo pairs correctly - a stereo pair is only deleted if both channels are
empty.

Menus:
Right-click a sequence in the Media Panel -> Sequence... -> Delete All Empty Tracks
"""

import flame

SCRIPT_NAME = "Delete Empty Tracks"
FOLDER = "Sequence..."


def delete_empty_video_tracks(selection):
    for clip in selection:
        for version in clip.versions:
            skip_next = False
            for track in version.tracks:
                if skip_next:
                    skip_next = False
                    continue
                if len(track.segments) == 1 and track.segments[0].type == "Gap":
                    skip_next = version.stereo
                    flame.delete(track)


def delete_empty_audio_tracks(selection):
    for clip in selection:
        for audio_track in clip.audio_tracks:
            skip_next = False
            for channel in audio_track.channels:
                if skip_next:
                    skip_next = False
                    continue
                if len(channel.segments) == 1 and channel.segments[0].type == "Gap":
                    skip_next = audio_track.stereo
                    flame.delete(channel)


def delete_all_empty_tracks(selection):
    delete_empty_video_tracks(selection)
    delete_empty_audio_tracks(selection)


def scope_sequence(selection):
    for item in selection:
        if isinstance(item, flame.PySequence):
            return True
    return False


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": FOLDER,
            "actions": [
                {
                    "name": "Delete All Empty Tracks",
                    "isVisible": scope_sequence,
                    "execute": delete_all_empty_tracks,
                    "minimumVersion": "2021.1.0.0"
                }
            ]
        }
    ]
