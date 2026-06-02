"""
Script Name: Create Reel Group
Script Version: 1.0
Flame Version: 2021.1
Written by: Bryan Bayley
Creation Date: 04.25.19

Description:
Create a standardized Online Assemble reel group inside a selected library,
pre-configured with _Sources Sequence, Sources, and Conform reels.

Menus:
Right-click a Library in the Media Panel -> Create Reel Group -> Create ReelGroup for Online Assemble
"""

import flame


def create_reel_group(selection):
    for item in selection:
        reel_group = item.create_reel_group("Online Assemble")
        reel_group.colour = 50, 0, 0
        reel = reel_group.create_reel("_Sources Sequence", sequence=True)
        reel.colour = 0, 0, 0
        reel = reel_group.create_reel("Sources")
        reel.colour = 29, 67, 45
        reel = reel_group.create_reel("Conform", sequence=True)
        reel.colour = 96, 12, 12

        for reel in reel_group.reels:
            if "Reel" in str(reel.name) or "Sequences" in str(reel.name):
                flame.delete(reel)


def scope_library(selection):
    for item in selection:
        if isinstance(item, flame.PyLibrary):
            return True
    return False


def get_media_panel_custom_ui_actions():
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
