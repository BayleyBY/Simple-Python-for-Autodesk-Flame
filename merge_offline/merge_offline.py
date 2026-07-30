"""
Script Name: Merge Offline
Script Version: 1.0
Flame Version: 2026
Written by: Bryan Bayley
Help from: Fred Warren
Creation Date: 07.29.23

Description:
Automates merging an offline edit (AAF/XML/EDL) with a reference video for
online comparison. Stacks the offline edit above the reference, sets
primary/secondary tracks for A/B comparison, locks the reference video and
audio, adds virtual padding and a black top track, and deletes the
standalone reference clip from the Media Panel.

Prerequisites:
- Import the AAF/XML/EDL to a sequence reel.
- Import the reference video to the same sequence reel, named
  <sequence_name>_OFFLINE, with the same start frame as the offline edit
  (e.g. don't have the offline edit start on the first frame of picture
  while the reference video has a 2-pop).
- This script uses flame.execute_shortcut(). The shortcuts used must still
  exist in the Keyboard Shortcut editor (they do by default): Nudge 1 Track
  Up, Nudge 1 Track Down, Overwrite Edit, Timeline Home, Set Focus on
  Topmost Visible Track.

Menus:
Right-click a sequence in the Media Panel -> Sequence... -> Merge Offline
"""

import flame


def scope_clip(selection):
    for item in selection:
        if isinstance(item, flame.PyClip):
            return True
    return False


def merge_offline(selection):
    for clip in selection:
        # Find the reference clip before touching the sequence so a missing
        # reference leaves the sequence untouched.
        clip_name = str(clip.name)[1:-1]
        ref = None
        for item in flame.find_by_name(clip_name + "_OFFLINE"):
            ref = item
        if ref is None:
            print("Merge Offline: no clip named '%s_OFFLINE' found - skipping '%s'" % (clip_name, clip_name))
            continue

        # Make sure the clip is open as a sequence
        clip.open()

        # Get the number of tracks in the AAF/XML/EDL
        num_tracks = len(clip.versions[0].tracks)

        # Move the segments up with the "Nudge 1 Track Up" shortcut - a hack
        # because tracks cannot be patched directly. An extra Nudge Up and
        # Nudge Down leaves a blank track on top for the black padding later.
        for track in range(num_tracks):
            clip.versions[0].tracks[track].selected_segments = clip.versions[0].tracks[track].segments
        flame.execute_shortcut("Nudge 1 Track Up")
        flame.execute_shortcut("Nudge 1 Track Up")
        flame.execute_shortcut("Nudge 1 Track Down")

        # Add a stereo audio track for the incoming reference audio
        clip.create_audio(stereo=True)

        # Overwrite the reference video onto the bottom track and its audio
        # onto the new audio track
        clip.primary_track = clip.versions[0].tracks[0]
        flame.media_panel.selected_entries = [ref]
        flame.execute_shortcut("Overwrite Edit")

        # Set primary (top) / secondary (bottom) tracks and lock the
        # reference video and audio
        clip.primary_track = clip.versions[0].tracks[num_tracks]
        clip.secondary_track = clip.versions[0].tracks[0]
        clip.versions[0].tracks[0].locked = True
        clip.audio_tracks[0].channels[0].locked = True

        # Clear in and out marks
        clip.in_mark = None
        clip.out_mark = None

        # Add virtual padding to start and end
        clip.padding_start = flame.PyTime("00:59:59:00", "23.976 fps")
        clip.padding_end = flame.PyTime(int(clip.duration.frame) + 25)

        # Add black (virtual colour) on the top track and cut it to the
        # picture-only range
        top_track = len(clip.versions[0].tracks) - 1
        clip.versions[0].tracks[top_track].segments[0].set_gap_colour(0, 0, 0)
        clip.versions[0].tracks[top_track].segments[0].colour = (0, 0, 0)
        frame_one = flame.PyTime("01:00:00:00", "23.976 fps")
        end_frame = flame.PyTime(int(clip.duration.frame) - 23)
        clip.versions[0].tracks[top_track].cut(frame_one)
        clip.versions[0].tracks[top_track].cut(end_frame)
        flame.delete(clip.versions[0].tracks[top_track].segments[1])

        # Move the playhead to the start of the sequence, frame the whole
        # sequence, move focus to the top track
        clip.current_time = flame.PyTime(1)
        flame.execute_shortcut("Timeline Home")
        flame.execute_shortcut("Set Focus on Topmost Visible Track")

        # Delete the standalone reference clip
        flame.media_panel.selected_entries = [clip]
        flame.delete(ref)


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": "Sequence...",
            "actions": [
                {
                    "name": "Merge Offline",
                    "isVisible": scope_clip,
                    "execute": merge_offline
                }
            ]
        }
    ]
