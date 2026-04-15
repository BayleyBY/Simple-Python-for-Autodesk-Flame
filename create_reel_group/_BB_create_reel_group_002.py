'''
Script Name: Create Reel Group
Script Version: 1.0
Flame Version: 2021.1
Written by: Bryan Bayley
Creation Date: 2019.04.25
Update Date: 2021.08.02

Description: Create and color a Reel Group for Online Assemble / Finishing.
'''

def create_reel_group(selection):
    import flame
    for item in selection:
        reelGroup = item.create_reel_group("Online Assemble")
        reelGroup.colour = 50,0,0
        reel = reelGroup.create_reel("_Sources Sequence", sequence = True)
        reel.colour = 0,0,0
        reel = reelGroup.create_reel("Sources")
        reel.colour = 29,67,45
        reel = reelGroup.create_reel("Conform", sequence = True)
        reel.colour = 96,12,12
            
    for reels in reelGroup.reels:
        if "Reel" in str(reels.name) or "Sequences" in str(reels.name):
             flame.delete(reels)

def get_media_panel_custom_ui_actions():

    def scope_library(selection):
        import flame
        for item in selection:
            if isinstance(item, (flame.PyLibrary)):
                return True
        return False

    return [
         {
            "name": "Create Reel Group",
            "actions": [
                {
                    "name": "Create ReelGroup for Online Assemble",
                    "isVisible": scope_library,
                    "execute": create_reel_group
                }
            ]
        }
    ]
