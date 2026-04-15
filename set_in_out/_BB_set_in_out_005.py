'''
Script Name: Set In/Out Options
Script Version: 1.5
Flame Version: 2021.1
Written by: Bryan Bayley
Creation Date: 2021.07.29
Update Date: 2021.08.12

Description: Various options for setting the In/Out on clips depending on where it's going.
-- Clear all IN/Out Marks
-- 1 sec Head/Tail for Client Posting
-- Slate with No Tails for Broadcast Delivery
-- Slate with one sec tails for slated approvals
-- Frame-To-Frame for Online/Social videos
-- Republic Master - 2 seconds Head / Slate / Spot / 1 second tail

For all of these options:
-- clip must be 23.98/24
-- Slate at 59:53:00
-- First frame of picture at 1:00:00:00
-- 1 second black at end of sequence
'''

def clear_in_out(selection):
    import flame
    for clip in selection:
        clip.in_mark = None
        clip.out_mark = None

def in_out_posting(selection):
    import flame
    for clip in selection:
        clip.in_mark = None
        clip.out_mark = None
        clip.out_mark = int(clip.duration.frame)+1
        clip.in_mark = flame.PyTime("00:59:59:00", clip.frame_rate)

def in_out_slated_approval(selection):
    import flame
    for clip in selection:
        clip.in_mark = None
        clip.out_mark = None
        clip.out_mark = int(clip.duration.frame)+1
        clip.in_mark = flame.PyTime("00:59:53:00", clip.frame_rate)

def in_out_slated(selection):
    import flame
    for clip in selection:
        clip.in_mark = None
        clip.out_mark = None
        clip.out_mark = int(clip.duration.frame)-23
        clip.in_mark = flame.PyTime("00:59:53:00", clip.frame_rate)

def in_out_olv(selection):
    import flame
    for clip in selection:
        clip.in_mark = None
        clip.out_mark = None
        clip.out_mark = int(clip.duration.frame)-23
        clip.in_mark = flame.PyTime("01:00:00:00", clip.frame_rate)            

def in_out_republic_master(selection):
    import flame
    for clip in selection:
        clip.in_mark = None
        clip.out_mark = None
        clip.out_mark = int(clip.duration.frame)+1
        clip.in_mark = flame.PyTime("00:59:51:00", clip.frame_rate)

def get_media_panel_custom_ui_actions():

    def scope_clip(selection):
        import flame
        for item in selection:
            if isinstance(item, flame.PyClip):
                return True
        return False

    return [
        {
            'name': 'Set In-Out...',
            'actions': [
                
                {
                    'name': 'Clear All In-Out',
                    'isVisible': scope_clip,
                    'execute': clear_in_out,
                    'minimumVersion': '2022'
                },
                {
                    'name': 'Set In-Out for CLIENT POSTING',
                    'isVisible': scope_clip,
                    'execute': in_out_posting,
                    'minimumVersion': '2022'
                },
                {
                    'name': 'Set In-Out for SLATED APPROVALS',
                    'isVisible': scope_clip,
                    'execute': in_out_slated_approval,
                    'minimumVersion': '2022'
                },
                {
                    'name': 'Set In-Out for SLATED DELIVERY',
                    'isVisible': scope_clip,
                    'execute': in_out_slated,
                    'minimumVersion': '2022'
                },
                {
                    'name': 'Set In-Out for OLV-SOCIAL',
                    'isVisible': scope_clip,
                    'execute': in_out_olv,
                    'minimumVersion': '2022'
                },
                {
                    'name': 'Set In-Out for Republic Master',
                    'isVisible': scope_clip,
                    'execute': in_out_republic_master,
                    'minimumVersion': '2022'
                }
            ]
        }
    ]
