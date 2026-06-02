"""
Script Name: Cache Motion Vectors
Script Version: 1.0
Flame Version: 2021.1
Written by: Bryan Bayley
Creation Date: 08.11.19

Description:
In Batch, build the Action/Media node network needed to cache motion vectors
for a selected clip node and cache them across the full clip duration.

Menus:
Right-click a Clip node in Batch -> Cache... -> Cache Motion Vectors
"""

import flame


def get_context():
    contexts = flame.batch.contexts
    for context in range(1, 11):
        if context not in contexts:
            return context
    return None


def scope_node(selection):
    for item in selection:
        if isinstance(item, flame.PyNode) and item.type == "Clip":
            return True
    return False


def create_motion(selection):
    clip = flame.batch.current_node.get_value()
    action = flame.batch.create_node("Action")
    action.pos_x = clip.pos_x + 400
    action.pos_y = clip.pos_y
    media = action.add_media()
    media.pos_x = clip.pos_x + 200
    media.pos_y = clip.pos_y

    flame.batch.connect_nodes(clip, "Default", media, "Default")

    motion_map = action.create_node("Motion Vectors Map")

    start = flame.batch.start_frame.get_value()
    end = start + clip.duration.frame

    motion_map.cache_range(start, end)


def get_batch_custom_ui_actions():
    return [
        {
            "name": "Cache...",
            "actions": [
                {
                    "name": "Cache Motion Vectors",
                    "isVisible": scope_node,
                    "execute": create_motion
                }
            ]
        }
    ]
