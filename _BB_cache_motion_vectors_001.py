"""
Script Name: Cache Motion Vectors
Script Version: 1.1
Flame Version: 2021.1
Written by: Bryan Bayley
Creation Date: 2019.08.11
Update Date: 

A simplified version of the example script that only works on clips in batch (removed desktop function)


"""

def get_batch_custom_ui_actions():
    def scope_node(selection):
        import flame
        for item in selection:
            if isinstance(item, flame.PyNode):
                if item.type == "Clip":
                    return True
        return False

    def create_motion(selection):
        import flame

        clip = flame.batch.current_node.get_value()
        action = flame.batch.create_node("Action")
        pos_x = clip.pos_x
        pos_y = clip.pos_y
        action.pos_x = pos_x + 400
        action.pos_y = pos_y
        media = action.add_media()
        media.pos_x = pos_x +200
        media.pos_y = pos_y

        flame.batch.connect_nodes(clip, "Default", media, "Default")

        motion_map = action.create_node("Motion Vectors Map")

        start = flame.batch.start_frame.get_value()
        end = start + clip.duration.get_value()

        motion_map.cache_range(start, end)

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