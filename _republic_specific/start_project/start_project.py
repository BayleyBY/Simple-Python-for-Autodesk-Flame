"""
Script Name: Start Project
Script Version: 1.0
Flame Version: 2024.2.1
Written by: Bryan Bayley
Creation Date: 02.09.24

Description:
Full new-project setup in one click. Right-click on the WORKSPACE to access.
Individual actions:
- Clean Desktop: remove existing reel groups/batch groups, create 3 green reels.
- Rename Library: rename the default library to match the project name (red).
- Create Reel Group: create a standard Online Assemble reel group.
- Create Bookmarks: copy standard job folder bookmarks to the project.
- All The Things: run all four actions above.

Menus:
Right-click the Workspace in the Media Panel -> New Project Setup -> Clean Desktop
Right-click the Workspace in the Media Panel -> New Project Setup -> Clear and Rename Library
Right-click the Workspace in the Media Panel -> New Project Setup -> Create ReelGroup for Online
Right-click the Workspace in the Media Panel -> New Project Setup -> Create Standard Project Bookmarks
Right-click the Workspace in the Media Panel -> New Project Setup -> All The Things
"""

import os
import shutil
import flame


def clean_desktop(selection):
    desk = flame.project.current_project.current_workspace.desktop

    for reel_group in desk.reel_groups:
        flame.delete(reel_group)
    for batch_group in desk.batch_groups:
        flame.delete(batch_group)

    # Flame auto-creates a batch group when none exist — rename and recolor it.
    for batch_group in desk.batch_groups:
        batch_group.name = "Batch"
        batch_group.colour = 0, 0, 50

    reel_group = desk.create_reel_group("Reels")
    reel_group.colour = 0, 50, 0
    for name in ("Reel1", "Reel2", "Reel3"):
        reel = reel_group.create_reel(name)
        reel.colour = 29, 67, 45

    for reel in reel_group.reels:
        if "Sequences" in str(reel.name) or "Reel " in str(reel.name):
            flame.delete(reel)


def library_from_project(selection):
    project = flame.project.current_project
    library = project.current_workspace.libraries[0]
    library.name = project.name
    library.colour = 96, 12, 12

    for sequence in library.sequences:
        if "Sequence" in str(sequence.name):
            flame.delete(sequence)


def create_reel_group(selection):
    library = flame.project.current_project.current_workspace.libraries[0]
    reel_group = library.create_reel_group("Online Assemble")
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


def create_bookmarks(selection):
    project_name = str(flame.project.current_project.name)
    template_file = "/Volumes/Flame_Archive/_discreet/_bookmarks_standard_project/cf_bookmarks.xml"
    destination_dir = f"/opt/Autodesk/project/{project_name}/status"

    os.makedirs(destination_dir, exist_ok=True)
    shutil.copy(template_file, os.path.join(destination_dir, "cf_bookmarks.xml"))


def do_all(selection):
    clean_desktop(selection)
    library_from_project(selection)
    create_reel_group(selection)
    create_bookmarks(selection)


def scope_workspace(selection):
    for item in selection:
        if isinstance(item, flame.PyWorkspace):
            return True
    return False


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": "New Project Setup",
            "actions": [
                {
                    "name": "Clean Desktop",
                    "isVisible": scope_workspace,
                    "execute": clean_desktop
                },
                {
                    "name": "Clear and Rename Library",
                    "isVisible": scope_workspace,
                    "execute": library_from_project
                },
                {
                    "name": "Create ReelGroup for Online",
                    "isVisible": scope_workspace,
                    "execute": create_reel_group
                },
                {
                    "name": "Create Standard Project Bookmarks",
                    "isVisible": scope_workspace,
                    "execute": create_bookmarks
                },
                {
                    "name": "All The Things",
                    "isVisible": scope_workspace,
                    "execute": do_all
                }
            ]
        }
    ]
