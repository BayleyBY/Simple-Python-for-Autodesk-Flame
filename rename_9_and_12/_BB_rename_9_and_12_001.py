'''
Script Name: Rename Keep ID
Script Version: 1.0
Flame Version: 2020
Written by: Bryan Bayley
Help From: John Geehreng
Creation Date: 08.12.21

Description: Options to rename clips in the Media Panel to keep either 9 characters or 12 characters. 
                These are the two ID formats used for broadcast TVC delivery.

New Addition: Remove the last 22 characters (use to remove characters added by the premiere xml fixer)

'''

def keep_9(selection):
    import flame
    import re

    for item in selection:
        seq_name = str(item.name)[(1):-(1)]
        ad_id = seq_name[0:9]
        item.name = ad_id

def keep_12(selection):
    import flame
    import re

    for item in selection:
        seq_name = str(item.name)[(1):-(1)]
        ad_id = seq_name[0:12]
        item.name = ad_id

def remove_22(selection):
    import flame
    import re

    for item in selection:
        seq_name = str(item.name)[(1):-(1)]
        ad_id = seq_name[:-22]
        item.name = ad_id

def get_media_panel_custom_ui_actions():

    def scope_clip(selection):
        import flame
        for item in selection:
            if isinstance(item, flame.PyClip):
                return True
        return False

    return [
        {
            'name': "Rename...",
            'actions': [
                {
                    'name': "Keep 9 (FCB ID)",
                    'isVisible': scope_clip,
                    'execute': keep_9,
                    'minimumVersion': '2020'
                },
                {
                    'name': "Keep 12 (AD-ID)",
                    'isVisible': scope_clip,
                    'execute': keep_12,
                    'minimumVersion': '2020'
                },
                {
                    'name': "Remove Last 22",
                    'isVisible': scope_clip,
                    'execute': remove_22,
                    'minimumVersion': '2020'
                }
            ]
        }
    ]
