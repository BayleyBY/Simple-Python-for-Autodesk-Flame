'''
Script Name: Create Marker with Segment Duration
Script Version: 1.0
Flame Version: 2021.1
Written by: Bryan Bayley
Creation Date: 08.12.21

Description: Create a Marker or Segment Marker with duration of the segment
'''

def create_marker(selection):
    import flame
    for item in selection:
        parent = item.parent
        while ((isinstance(parent, (flame.PyClip)) != True) and parent):
            parent = parent.parent
        duration = item.record_duration
        marker = parent.create_marker(item.record_in)
        marker.duration = duration

def create_seg_marker(selection):
    import flame
    for item in selection:
        duration = item.record_duration
        marker = item.create_marker(item.record_in)
        marker.duration = duration

def get_timeline_custom_ui_actions():
    def scope_segment(selection):
        import flame
        for item in selection:
            if isinstance(item, (flame.PySegment)):
                return True
            return False

    return [
         {
            "name": "MARKERS...",
            "actions": [
                {
                    "name": "Create Marker on Segment Duration",
                    "isVisible": scope_segment,
                    "execute": create_marker
                },
                {
                    "name": "Create Segment Marker on Segment Duration",
                    "isVisible": scope_segment,
                    "execute": create_seg_marker
                },
            ]
        }
    ]
