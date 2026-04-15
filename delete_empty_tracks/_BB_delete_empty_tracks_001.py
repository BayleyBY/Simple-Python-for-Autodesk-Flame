"""
Script Name: Delete Empty Tracks
Script Version: 1.0
Flame Version: 2022.1
Written by: Bryan Bayley
Creation Date: 2021.08.11
Update Date: 2021.08.11

Description: Deletes empty tracks in all selected sequences. This will delete both audio and video tracks.

"""

def delete_empty_video_tracks(selection):
    import flame

    for clip in selection:
        for version in clip.versions:
            skip_next_chn = False
            for track in version.tracks:
                if skip_next_chn:
                    skip_next_chn = False
                    continue
                if len(track.segments) == 1 and track.segments[0].type == "Gap":
                   skip_next_chn = version.stereo
                   flame.delete(track)

def delete_empty_audio_tracks(selection):
    import flame

    for clip in selection:
        for audio_track in clip.audio_tracks:
            skip_next_chn = False
            for channel in audio_track.channels:
                if skip_next_chn:
                    skip_next_chn = False
                    continue
                if len(channel.segments) == 1 and channel.segments[0].type == "Gap":
                    skip_next_chn = audio_track.stereo
                    flame.delete(channel)

def delete_all_empty_tracks(selection):
    delete_empty_video_tracks(selection)
    delete_empty_audio_tracks(selection)

def get_media_panel_custom_ui_actions():

    def scope_clip(selection):
        import flame
        for item in selection:
            if isinstance(item, flame.PySequence):
                return True
        return False

    return [
        {
            "name": "Sequence...",
            "actions": [
                {
                    "name": "Delete All Empty Tracks",
                    "isVisible": scope_clip,
                    "execute": delete_all_empty_tracks,
                    "minimumVersion": "2021.1.0.0"
                }
            ]
        }
    ]
