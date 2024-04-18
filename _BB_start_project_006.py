'''
Script Name: Start Project
Script Version: 5.0
Flame Version: 2024.2.1
Written by: Bryan Bayley
Creation Date: 2024.02.09

Description: A set of functions that modify a new project. Access all of these by right clicking on the WORKSPACE 

- Clear the Desktop and create 3 Reels with Green color.
- Change the Library name to match the Project name and make it red.
- Create and color a Reel Group for Online Assemble / Finishing.
- Copy all the standard job folder bookmarks to this project
- Do All The Things Above

'''

#################
# Clean Desktop #
#################

def clean_desktop(desktop):
    import flame

    desk = flame.project.current_project.current_workspace.desktop

    # Delete any current Reel Groups
    for reel_groups in desk.reel_groups:
        flame.delete(reel_groups)

    # Delete any current Batch Groups    
    for batch_group in desk.batch_groups:
        flame.delete(batch_group)

    # When there are no Batch Groups, flame automatically creates one. 
    # This will rename it from "New Batch" to "Batch" and color it blue.
    for batch_group in desk.batch_groups:
        batch_group.name = "Batch"
        batch_group.colour = 0,0,50

    # This will Create a new Reel Group. Flame automatically adds three reels and a sequence reel. 
    # We will delete those next, while this creates our own 3 Reels with green color      
    reelGroup = desk.create_reel_group("Reels")
    reelGroup.colour = 0,50,0
    reel = reelGroup.create_reel("Reel1")
    reel.colour = 29,67,45
    reel = reelGroup.create_reel("Reel2")
    reel.colour = 29,67,45
    reel = reelGroup.create_reel("Reel3")
    reel.colour = 29,67,45

    # This will delete the default Reels and Sequence Reel created above
    for reels in reelGroup.reels:
        if "Sequences" in str(reels.name) or "Reel " in str(reels.name):
            flame.delete(reels)

############################
# Clear and Rename Library #
############################

def library_from_project(selection):
    import flame

    project = flame.project.current_project
    default_library = flame.project.current_project.current_workspace.libraries[0]
    
    default_library.name = project.name
    default_library.colour = 96,12,12
 
    for sequence in default_library.sequences:
        if "Sequence" in str(sequence.name):
            flame.delete(sequence)


#####################
# Create Reel Group #
#####################

def create_reel_group(selection):
    import flame
    for flame.project.current_project.current_workspace.libraries[0] in selection:
        reelGroup = flame.project.current_project.current_workspace.libraries[0].create_reel_group("Online Assemble")
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

####################
# Create Bookmarks #
####################

def create_bookmarks(selection):
    import flame
    import os
    import shutil

    project_name = flame.project.current_project.name

    # Define the path to the template file
    template_file = '/Volumes/Flame_Archive/_discreet/_bookmarks_standard_project/cf_bookmarks.xml'

    # Construct the destination directory where you want to copy the template file
    destination_directory = f"/opt/Autodesk/project/{project_name}/status"

    # Ensure the destination directory exists; create it if it doesn't
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Construct the destination path where you want to copy the template file
    destination_path = os.path.join(destination_directory, 'cf_bookmarks.xml')

    # Copy the template file to the destination path
    shutil.copy(template_file, destination_path)

#####################
# Do All The Things #
#####################

def do_all(selection):
    clean_desktop(selection)
    library_from_project(selection)
    create_reel_group(selection)
    create_bookmarks(selection)

#################
# Context Menus #
#################

def get_media_panel_custom_ui_actions():

    def scope_workspace(selection):
        import flame
        for item in selection:
            if isinstance(item, flame.PyWorkspace):
                return True
        return False

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
                {    "name": "All The Things",
                    "isVisible": scope_workspace,
                    "execute": do_all
                }
            ]
        }
    ]










