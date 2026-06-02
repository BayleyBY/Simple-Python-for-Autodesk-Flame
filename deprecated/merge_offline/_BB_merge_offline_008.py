'''
Script Name: Merge Offline
Script Version: 6.0
Flame Version: 2024
Written by: Bryan Bayley
Help from: Fred Warren
Creation Date: 07.29.23
Updated : 02.13.24

This script automates the process of merging an AAF/XML/EDL with a reference video.
- import the AAF/XML/EDL to a sequence reel
- import the reference video to the same sequence reel.
- the reference video must be named the same as the AAF/EDL/XML with "_ref" added to the end.
- the reference video needs to have the same start frame as the AAF/XML/EDL. e.g. don't have the AAF/XML/EDL start on
    the first frame of picture and the reference video have a 2-pop.
- Select the AAF/XML/EDL sequence and run the script. This will:
--- Add a track to original version.
--- Move each track up one layer.
--- Add stereo audio track.
--- Insert the reference video to the bottom track and audio to the audio track.
--- Clean up empty tracks and lock the reference video / audio.
--- Make the top track the primary track and the bottom track the secondary track for comparing offline to online.
--- Delete the reference video in the sequence reel.
- This script uses flame.execute_shortcut(). The shortcuts used in the script should already have a shortuct entry. 
    You will only be affected if you have deleted the shortcut keys for: 'Overwrite Edit' and 'Swap Selected'.
'''

import flame

def merge_offline(selection):

    for clip in selection:
        #Make sure the clip is open as a Sequence
        clip.open()
        
        #Get the number of tracks in the AAF/XML/EDL
        num_tracks = len(flame.timeline.clip.versions[0].tracks)

        # Move the AAF/XML/EDL segments up with "Nudge 1 Track Up" keyboard shortcut. This is a hack because we cannot directly patch tracks. 
        # An extra Nudge Up and Nudge Down leaves us with a blank track on top for adding black padding later.
        for track in range(num_tracks): 
            clip.versions[0].tracks[track].selected_segments = clip.versions[0].tracks[track].segments
        flame.execute_shortcut("Nudge 1 Track Up")
        flame.execute_shortcut("Nudge 1 Track Up")
        flame.execute_shortcut("Nudge 1 Track Down")
        
        # Add a stereo audio track for the incoming offline reference video
        clip.create_audio(stereo=True)

        #Search for a clip that has the same name as the AAF/XML/EDL with _ref at the end and Overwite it to the bottom track.
        clipname = clip.name
        clip.primary_track = clip.versions[0].tracks[0] 
        for ref in flame.find_by_name(clipname + "_ref"):
            flame.media_panel.selected_entries = [ref]
        flame.execute_shortcut("Overwrite Edit")

        # Change the primary/secondary tracks and lock the reference video/audio
        clip.primary_track = clip.versions[0].tracks[num_tracks]   #Set the primary track to top layer
        clip.secondary_track = clip.versions[0].tracks[0]  #Set the secondary track to bottom layer
        clip.versions[0].tracks[0].locked = True          #Lock the ref track
        clip.audio_tracks[0].channels[0].locked = True
        
        # Clear In and Out
        clip.in_mark = None
        clip.out_mark = None
        
        # Add Virtual Padding to Start and End
        clip.padding_start = flame.PyTime("00:59:59:00", "23.976 fps")
        clip.padding_end = flame.PyTime(int(clip.duration.frame)+25)

        # Add Black (Virtual Color) at the top track
        num_tracks = (len(flame.timeline.clip.versions[0].tracks) -1)
        clip.versions[0].tracks[num_tracks].segments[0].set_gap_colour(0,0,0)
        clip.versions[0].tracks[num_tracks].segments[0].colour=(0,0,0)
        frame_one = flame.PyTime("01:00:00:00", "23.976 fps")
        end_frame = flame.PyTime(int(clip.duration.frame)-23)
        clip.versions[0].tracks[num_tracks].cut(frame_one)
        clip.versions[0].tracks[num_tracks].cut(end_frame)
        flame.delete(clip.versions[0].tracks[num_tracks].segments[1])

        # Move the Play Head to the start of the sequence, frame the whole sequence, move focus to the top track.
        clip.current_time = flame.PyTime(1)
        flame.execute_shortcut("Timeline Home")
        flame.execute_shortcut("Set Focus on Top Visible Track")

        # Delete the _ref clip
        flame.media_panel.selected_entries = [clip]
        flame.delete(ref)

#############
### SCOPE ###
#############

def get_media_panel_custom_ui_actions():

    def scope_clip(selection):
        for item in selection:
            if isinstance(item, (flame.PyClip)):
                return True
        return False
            
    return [
         {
            "name": "Sequence...",
            "actions": [
                {
                    "name": "Merge Offline",
                    "isVisible": scope_clip,
                    "execute": merge_offline
                }
            ]
        }
    ]