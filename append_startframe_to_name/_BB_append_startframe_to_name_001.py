'''
Script Name: Append Start Frame to Name
Script Version: 1.0
Flame Version: 2023.1
Written by: Bryan Bayley
Help from: Michael Vaglienty
Creation Date: 2022.10.12
Update Date: 

Custom Action Type: Media Panel, Rename Clips

Description:
    - Get the Source Start Frame of the first segment in the clip.
    - Add this frame number to the end of the clip name.
    - The idea for this script is to add a unique identifier to clips that would 
        otherwise overwrite each other on export (due to having the same name).
    - This is standard procedure for Color Pass exports in other Color/Grading software.
'''

def startframe_to_name(selection):
    import flame
    import re

    for item in selection:
        if isinstance(item, flame.PyClip):
            source_frame = str(item.start_time.get_value().frame).zfill(8)
            seq_name = str(item.name)[1:-1]
            item.name = seq_name+"_"+source_frame

def get_media_panel_custom_ui_actions():

    def scope_clip(selection):
        import flame
        for item in selection:
            if isinstance(item, flame.PyClip):
                return True
        return False

    return [
        {
            'name': 'Rename...',
            'actions': [
                {
                    'name': 'Append Start Frame to Name',
                    'isVisible': scope_clip,
                    'execute': startframe_to_name,
                    'minimumVersion': '2020'
                }
            ]
        }
    ]
