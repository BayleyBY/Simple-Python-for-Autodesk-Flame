'''
Script Name: Black Head and Tail
Script Version: 1.5
Flame Version: 2022.1
Written by: Bryan Bayley
Help from: Fred Warren
Creation Date: 2021.08.16
Update Date: 2021.08.16

Add one second of virtual black head and tail to a sequence.
-- Start with a Colour Source (Black) on the desktop, 1 second duration, named "BLACK"
-- Make sure your sequences all have the patching set to which track you want to put it in.  We can't control the patching with Python for now.
-- The heads black will be insterted at 59:59:00 - 1:00:00:00
-- The Tails black will be inserted after the last frame
'''

def black_head_tail(selection):
    import flame
    
    for clip in selection:
        
        ''' Make sure the clip is opened as a Sequence'''
        clip.open()
        
        ''' Set in and out marks for the Head Black '''
        for clip in selection:
            clip.in_mark = None
            clip.out_mark = None
            clip.in_mark = flame.PyTime("00:59:59:00", clip.frame_rate)
            clip.out_mark = flame.PyTime("01:00:00:00", clip.frame_rate)
 
        ''' Search for a clip with the name "BLACK" and use it next '''
        for ref in flame.find_by_name("BLACK"):
            flame.media_panel.selected_entries = [ref]
        
        ''' Using flame.execute_shortcut... overwrite Black clip into the sequence. '''
        flame.execute_shortcut("Overwrite Edit")
            
        ''' Set in and out marks for the Tails Black '''
        for clip in selection:
            clip.in_mark = None
            clip.out_mark = None
            clip.in_mark = int(clip.duration.frame)+1
            
        ''' Search for a clip with the name "BLACK" and use it next'''
        for ref in flame.find_by_name("BLACK"):
            flame.media_panel.selected_entries = [ref]
        
        ''' Using flame.execute_shortcut... overwrite Black clip into the sequence.'''
        flame.execute_shortcut("Overwrite Edit")

        # Move the Play Head to the start of the sequence, frame the whole sequence, move focus to the top track.
        clip.current_time = flame.PyTime(1)
        flame.execute_shortcut("Timeline Home")
        flame.execute_shortcut("Set Focus on Top Visible Track")

def get_media_panel_custom_ui_actions():

    def scope_clip(selection):
        import flame
        for item in selection:
            if isinstance(item, flame.PyClip):
                return True
        return False

    return [
        {
            'name': 'Sequence...',
            'actions': [
                {
                    'name': 'Black Heads and Tails',
                    'isVisible': scope_clip,
                    'execute': black_head_tail,
                }
            ]
        }
    ]
