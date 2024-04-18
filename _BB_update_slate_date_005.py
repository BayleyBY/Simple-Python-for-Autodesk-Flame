'''
Script Name: Udpate Slate Date
Script Version: 1.5
Flame Version: 2021
Written by: Bryan Bayley
Help From: Fred Warren, Philippe Jean
Creation Date: 08.10.21
Updated: 08.13.21

Custom Action Type: Timeline Segments, Burn-in Metadata effect.

Description:
	In all selected Sequences, update the Burn-in Metadata timeline effects to show current date.
	I use this to update slate dates.
    
    This script uses flame.execute_shortcut() which introduces some limitations:
    For this to work you must create a hotkey for the "Update" button in the Burn-In Metadata>>Layer Specific soft effect menu.
    For the hotkey to be created you have to assign a key/key combination. But once it is created you can clear the key.  It doesn't have to be mapped to a button, just create the hotkey entry.
    The Burn-In Metadata soft effect must be on a segment (or gap segment) with no other soft effects.
    Before running the script, make sure your first sequence has the segment with Burn-In Metadata effect selected and the "Layer Specific" menu is visible.
'''
def update_burnin(selection):
    import flame
    for shot in selection:
        shotname = shot.name.get_value()
        try:
            shot = shot.open_as_sequence()
            for version in shot.versions:
                for track in version.tracks:
                    for segment in track.segments:
                        for tlfx in segment.effects:
                            if tlfx.type == 'Burn-in Metadata':
                                shot.selected_segments = [segment]
                                flame.execute_shortcut ("Update")
        except:
            print("Had issues with %s"%(shotname))
            
def get_media_panel_custom_ui_actions():

    def scope_seq(selection):
        import flame
        for item in selection:
            if isinstance(item, flame.PySequence):
                return True
        return False
 
    return [
        {
            'name': 'Slates...',
            'actions': [
                {
                    'name': 'Update Slate Date',
                    'isVisible': scope_seq,
                    'execute': update_burnin,
                    'minimumVersion': '2021'
                }
            ]
        }
    ]
