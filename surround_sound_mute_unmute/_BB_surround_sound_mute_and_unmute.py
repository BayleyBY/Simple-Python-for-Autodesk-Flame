'''
Script Name: Surround Sound Channels Mute
Script Version: 1.0
Flame Version: 2020
Written by: John Geehreng

MUTE AND UNMUTE Scripts combined by Bryan Bayley

Creation Date: 06.06.20
Update Date: 04.27.23

Custom Action Type: MediaPanel

Description:

    Mute / Unmute audio tracks 1-6 on all selected clips/sequences.
'''

def mute_channels(selection):
    import flame

    for item in selection:

        atrack = item.audio_tracks[0]
        atrack.mute = True
        atrack = item.audio_tracks[1]
        atrack.mute = True
        atrack = item.audio_tracks[2]
        atrack.mute = True
        atrack = item.audio_tracks[3]
        atrack.mute = True
        atrack = item.audio_tracks[4]
        atrack.mute = True
        atrack = item.audio_tracks[5]
        atrack.mute = True

def unmute_channels(selection):
    import flame

    for item in selection:

        atrack = item.audio_tracks[0]
        atrack.mute = False
        atrack = item.audio_tracks[1]
        atrack.mute = False
        atrack = item.audio_tracks[2]
        atrack.mute = False
        atrack = item.audio_tracks[3]
        atrack.mute = False
        atrack = item.audio_tracks[4]
        atrack.mute = False
        atrack = item.audio_tracks[5]
        atrack.mute = False

def scope_clip(selection):
    import flame

    for item in selection:
        if isinstance(item, flame.PyClip):
            return True
    return False

def get_media_panel_custom_ui_actions():

    return [
        {
            'name': 'Audio',
            'actions': [
                {
                    'name': 'Mute Surround Channels',
                    'isVisible': scope_clip,
                    'execute': mute_channels,
                    'minimumVersion': '2020'
                },
                {
                    'name': 'UnMute Surround Channels',
                    'isVisible': scope_clip,
                    'execute': unmute_channels,
                    'minimumVersion': '2020'
                }
            ]
        }
    ]
