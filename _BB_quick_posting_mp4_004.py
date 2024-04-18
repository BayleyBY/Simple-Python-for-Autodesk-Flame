'''
Script Name: Quick Posting MP4
Script Version: 1.0
Flame Version: 2024
Written by: Bryan Bayley
Creation Date: 2023.05.05
Update Date: 2023.05.11

Notes:
- This script exports selected clips to the job folder / Postings folder.  
- It creates a new dated folder, rounding the minutes to the nearest 15min increment.
- Facilis Partitions must be mounted at /Volumes
- Flame Project Nickname must be the Facilis partition name (ex: Republic_2023_Q1)
- Flame Project Name must match the job folder (ex: R2305590_Client_Project)
- After Export, the script will trigger a process that uses ffmpeg to remux the .mov to .mp4.
- This is a remux, not just renaming the file extension.
- AAC audio must be used to avoid sync issues.
- A shortened path is placed in the copy buffer. This path is everything after the Project Job Folder (02_Exports/01_Postings/02_Online/<dated>). You can paste this to share with other people (such as slack).
'''

from PySide2 import QtWidgets
import flame, datetime, re, fnmatch, os, subprocess, time 

def export_clips(selection):

    def token_path(clip, export_path):

        global new_export_path
        global quicktime_name

        date = datetime.datetime.now()
        approx = round(date.minute/15.0) * 15
        date = date.replace(minute=0)
        date += datetime.timedelta(seconds=approx * 60)
        time = date.time()
        clip_name = str(clip.name)[1:-1]

        quicktime_name = clip_name+".mov"

        new_export_path = re.sub('<ProjectName>', flame.project.current_project.name, export_path)
        new_export_path = re.sub('<ProjectNickName>', flame.project.current_project.nickname, new_export_path)
        new_export_path = re.sub('<YYYY>', date.strftime('%Y'), new_export_path)
        new_export_path = re.sub('<YY>', date.strftime('%y'), new_export_path)
        new_export_path = re.sub('<MM>', date.strftime('%m'), new_export_path)
        new_export_path = re.sub('<DD>', date.strftime('%d'), new_export_path)
        new_export_path = re.sub('<Hour>', date.strftime('%H'), new_export_path)
        new_export_path = re.sub('<Minute>', time.strftime('%M'), new_export_path)
        new_export_path = re.sub('<AMPM>', date.strftime('%p'), new_export_path)

        return new_export_path

    clip_output = flame.PyExporter()
    for clip in selection:
        clip_output.use_top_video_track = True
        clip_output.foreground = True
        clip_output.export_between_marks = True
        new_export_path = token_path(clip, '/Volumes/<ProjectNickName>/<ProjectName>/03_Exports/01_Postings/02_Online/<YY>-<MM>-<DD>-<Hour><Minute>/')

        if not new_export_path:
            return
        if not os.path.isdir(new_export_path):
            os.makedirs(new_export_path)

        clip_output.export(clip, '/opt/Autodesk/shared/export/presets/movie_file/Quick_Posting_MP4.xml', new_export_path)

        flame.go_to('MediaHub')
        flame.mediahub.files.set_path(new_export_path)

        #Remove /Volumes/<mount>/<job name>/ 
        folders = new_export_path.split("/")
        slack_path = "/".join(folders[4:])
        slack_path = slack_path.rsplit('/', 1)[0]
        
        # Add clip path to clipboard
        qt_app_instance = QtWidgets.QApplication.instance()
        qt_app_instance.clipboard().setText(slack_path)


def scope_clip(selection):
    for item in selection:
        if isinstance(item, flame.PyClip):
            return True
    return False

def get_media_panel_custom_ui_actions():
    return [{'name': 'Export...',
            'actions': 
            [{
                    'name': 'Quick Posting MP4',
                    'isVisible': scope_clip,
                    'execute': export_clips,
                    'minimumVersion': '2022'
            }]}]

# This prevents the post_export_sequence hook from running this function unless it is called from this specific script.
trigger_hook = True

### Flame Hook to execute a script after an export is done.
def post_export_sequence(info, userData, *args, **kwargs):
    
    if not trigger_hook:
        return  # Skip the function entirely if trigger_hook is False

    remux_source = os.path.join(new_export_path, quicktime_name)
    remux_dest   = os.path.join(new_export_path, os.path.splitext(quicktime_name)[0] + ".mp4" )
    ffmpeg_cmd = ['/usr/local/bin/ffmpeg', '-y', '-i', remux_source, '-codec:v', 'copy', '-codec:a', 'aac', '-ab', '320k', remux_dest]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    # Remove the source file if the destination file got created and isn't empty
    if( os.path.isfile(remux_dest) ):
        if( os.path.getsize(remux_dest) > 0 ):
            os.remove( remux_source )
            print("======= MP4 created successfully and MOV was deleted. =======")
        else:
            print("======= MP4 REMUX DID NOT COMPLETE =======")