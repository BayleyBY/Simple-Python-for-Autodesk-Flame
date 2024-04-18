'''
Script Name: Clip path to clipboard for Slack
Script Version: 2.0
Flame Version: 2024
Written by: Michael Vaglienty
Modified for shortened paths by: Bryan Bayley
Creation Date: 06.16.19
Update Date: 04.27.23

Custom Action Type: Timeline / Media Panel / Media Hub / Batch

Description:

    Copy clip path to clipboard. Removes /Volumes/<mount>/<project> to shorten links when sharing.

'''

from __future__ import print_function

VERSION = 'v2.0'

def media_panel_copy_path(selection):
    from PySide2 import QtWidgets

    clip_paths = ''

    clip_list = [clip.versions[0].tracks[0].segments[0].file_path.rsplit('/', 1)[0] for clip in selection if clip.versions[0].tracks[0].segments[0].file_path]

    # Convert path list to string with new line
    for clip in clip_list:
        clip_paths += clip + '\n'

    # Add clips to clipboard
    qt_app_instance = QtWidgets.QApplication.instance()
    qt_app_instance.clipboard().setText(clip_paths)

def timeline_copy_path(selection):
    from PySide2 import QtWidgets

    clip_paths = ''

    clip_list = [clip.file_path.rsplit('/', 1)[0] for clip in selection if clip.file_path]

    # Convert path list to string with new line
    for clip in clip_list:
        clip_paths += clip + '\n'

    # Add clips to clipboard
    qt_app_instance = QtWidgets.QApplication.instance()
    qt_app_instance.clipboard().setText(clip_paths)

def batch_copy_path(selection):
    from PySide2 import QtWidgets

    clip_paths = ''

    clip_list = [str(clip.media_path)[1:-1].rsplit('/', 1)[0] for clip in selection if clip.media_path != '']

    # Convert path list to string with new line
    for clip in clip_list:
        clip_paths += clip + '\n'

    # Add clips to clipboard
    qt_app_instance = QtWidgets.QApplication.instance()
    qt_app_instance.clipboard().setText(clip_paths)

def mediahub_copy_path(selection):
    from PySide2 import QtWidgets

    clip = selection[0]

    clip_path = clip.path.rsplit('/', 1)[0]

    if clip_path != '':

        # Add clip path  to clipboard
        qt_app_instance = QtWidgets.QApplication.instance()
        qt_app_instance.clipboard().setText(clip_path)

def mediahub_copy_shortpath(selection):
    from PySide2 import QtWidgets

    clip = selection[0]

    clip_path = clip.path

    if clip_path != '':
    
        #Remove /Volumes/<mount>/<job name>/ 
        folders = clip_path.split("/")
        slack_path = "/".join(folders[4:])
        slack_path = slack_path.rsplit('/', 1)[0]

        # Add clip path to clipboard
        qt_app_instance = QtWidgets.QApplication.instance()
        qt_app_instance.clipboard().setText(slack_path)

# Scopes
#-------------------------------------#

def scope_timeline_clip(selection):
    import flame

    for item in selection:
        if isinstance(item, flame.PySegment):
            if item.file_path != '':
                return True
    return False

def scope_batch_clip(selection):
    import flame

    for item in selection:
        if item.type == 'Clip':
            clip_path = str(item.media_path)[1:-1].rsplit('/', 1)[0]
            if clip_path != '':
                return True
    return False

def scope_clip(selection):
    import flame

    for item in selection:
        if isinstance(item, flame.PyClip):
            if item.versions[0].tracks[0].segments[0].file_path != '':
                return True
    return False

def scope_file(selection):
    import flame
    import re

    for item in selection:
        item_path = str(item.path)
        item_ext = re.search(r'\.\w{3}$', item_path, re.I)
        if item_ext != (None):
            return True
    return False

#-------------------------------------#

def get_media_panel_custom_ui_actions():

    return [
        {
            'name': 'File Path...',
            'actions': [
                {
                    'name': 'Copy Path to Clipboard',
                    'isVisible': scope_clip,
                    'execute': media_panel_copy_path,
                    'minimumVersion': '2021'
                }
            ]
        }
    ]

def get_batch_custom_ui_actions():

    return [
        {
            'name': 'File Path...',
            'actions': [
                {
                    'name': 'Copy Path to Clipboard',
                    'isVisible': scope_batch_clip,
                    'execute': batch_copy_path,
                    'minimumVersion': '2021'
                }
            ]
        }
    ]

def get_mediahub_files_custom_ui_actions():

    return [
        {
            'name': 'File Path...',
            'actions': [
                {
                    'name': 'Copy Full Path to Clipboard',
                    'isVisible': scope_file,
                    'execute': mediahub_copy_path,
                    'minimumVersion': '2021'
                },
                {
                    'name': 'Copy Short Path to Clipboard',
                    'isVisible': scope_file,
                    'execute': mediahub_copy_shortpath,
                    'minimumVersion': '2021'
                }
            ]
        }
    ]

def get_timeline_custom_ui_actions():

    return [
        {
            'name': 'File Path...',
            'actions': [
                {
                    'name': 'Copy Path to Clipboard',
                    'isVisible': scope_timeline_clip,
                    'execute': timeline_copy_path,
                    'minimumVersion': '2021'
                }
            ]
        }
    ]
