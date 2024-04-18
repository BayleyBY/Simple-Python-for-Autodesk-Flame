'''
Script Name: Color Timewarp Shots
Script Version: 1.0
Flame Version: 2021.1
Written by: Bryan Bayley
Creation Date: 08.12.21

Description: Color > Red to all segments with Timewarp Effect
'''

def color_timewarp_clip(selection):
    import flame
    for shot in selection:
        for version in shot.versions:
            for track in version.tracks:
                for segment in track.segments:
                    for tlfx in segment.effects:
                        if tlfx.type == 'Timewarp':
                            segment.colour = (96, 12, 12)

def get_media_panel_custom_ui_actions():

    def scope_seq(selection):
        import flame

        for item in selection:
            if isinstance(item, flame.PySequence):
                return True
        return False

    return [
        {
            'name': 'Sequence...',
            'actions': [
                {
                    'name': 'Color Timewarped Shots',
                    'isVisible': scope_seq,
                    'execute': color_timewarp_clip,
                    'minimumVersion': '2020'
                }
            ]
        }
    ]
