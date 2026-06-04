"""
Script Name: Import Open Clip
Script Version: 1.0
Flame Version: 2027
Written by: Bryan Bayley
Help from: Michael Vaglienty
Creation Date: 05.04.26

Script Type: Batch

Description:

    Import the open clip created by the selected Write File node into a Batch
    schematic reel.

    Token resolution supports the Flame 2027 token-slicing syntax (e.g. <shot name[0:-6]>)
    and sources <version name>/<version> from the write node's own versioning.

Menus:

    Right-click on a Write File node in Batch -> Import... -> Import Open Clip to Batch
"""

#-------------------------------------
# [Imports]
#-------------------------------------

import os
import re
import flame

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

#-------------------------------------
# [Constants]
#-------------------------------------

SCRIPT_NAME = "Import Open Clip to Batch"

# Destination Batch schematic reel for the imported open clip. Created
# automatically if it doesn't already exist. Edit to change the target reel.
SCHEMATIC_REEL = "Renders"

#-------------------------------------
# [UI]
#-------------------------------------

def message_box(message):
    """Show a simple modal dialog. Replaces PyFlameMessageWindow."""

    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle(SCRIPT_NAME)
    msg.setText(message)
    msg.exec_()

#-------------------------------------
# [Token Resolution]
#-------------------------------------

def apply_token_slice(value, slice_expr):
    """
    Apply a Flame 2027 token slice to a resolved token string.

    slice_expr is the bracketed portion of a token, e.g. '[:8]', '[9:15]',
    '[16:]', or '[-4:]'. Flame's documented slicing semantics match Python's
    own string slicing (0-based from the front, -1 from the end, start
    inclusive, stop exclusive, out-of-range values clamped), so we parse the
    bounds and let Python do the slice. Returns the unsliced value if the
    expression can't be parsed.
    """

    inner = slice_expr[1:-1].strip()  # strip surrounding [ ]
    bounds = inner.split(":")

    # A valid slice is 'x:y' (either side may be empty). Anything else is left
    # untouched rather than risk mangling the path.
    if len(bounds) != 2:
        return value

    try:
        start = int(bounds[0]) if bounds[0].strip() else None
        stop = int(bounds[1]) if bounds[1].strip() else None
    except ValueError:
        return value

    return value[start:stop]

def resolve_path_tokens(pattern, token_dict):
    """
    Replace Flame tokens in a path pattern with their resolved values, honoring
    the Flame 2027 token-slicing syntax (e.g. <shot name[:8]>, <name[9:15]>,
    <batch name[-4:]>).

    token_dict maps full token strings ('<shot name>') to their resolved
    values. Older releases wrote bare tokens with no brackets; this handles
    both, so it is safe on pre-2027 paths too.
    """

    # Map bare token names ('shot name') to values; the slice lives outside the
    # name in the path text, so we match on the name and apply the slice after.
    value_by_name = {token[1:-1]: value for token, value in token_dict.items()}

    # Longest names first so '<batch name>' matches before '<name>'.
    names = sorted(value_by_name, key=len, reverse=True)
    token_re = re.compile(
        r"<(" + "|".join(re.escape(name) for name in names) + r")(\[[^\]]*\])?>"
        )

    def _replace(match):
        value = value_by_name[match.group(1)]
        slice_expr = match.group(2)
        if slice_expr:
            value = apply_token_slice(value, slice_expr)
        return value

    return token_re.sub(_replace, pattern)

#-------------------------------------
# [Main Script]
#-------------------------------------

def translate_write_node_path(write_node):
    """
    Resolve the selected Write File node's create_clip_path tokens into the full
    path of the open clip (.clip) it writes.
    """

    print("Translating write node path...")

    media_path = str(write_node.media_path)[1:-1]
    print("    media path:", media_path)
    pattern = str(write_node.create_clip_path)[1:-1]
    print("    pattern:", pattern)

    # flame.project.current_project.name / .nickname return plain strings (not
    # quote-wrapped like clip/segment names), so no [1:-1] slicing here.
    project = str(flame.project.current_project.name)
    project_nickname = str(flame.project.current_project.nickname)
    batch_iteration = str(flame.batch.current_iteration.name)[1:-1]
    batch_name = str(flame.batch.name)[1:-1]
    ext = ""
    name = str(write_node.name)[1:-1]
    shot_name = str(write_node.shot_name)[1:-1]
    # <version name> and <version> come from the write node's own versioning so
    # they honour its Version Mode and Padding settings. version_name is a
    # string attr (quote-wrapped); version_number and version_padding are ints.
    # e.g. 'comp', 2, 3 -> 'comp' and '002'.
    version_name = str(write_node.version_name)[1:-1]
    version_padding = int(str(write_node.version_padding))
    version = str(write_node.version_number).zfill(version_padding)

    token_dict = {
        "<project>": project,
        "<project nickname>": project_nickname,
        "<batch iteration>": batch_iteration,
        "<batch name>": batch_name,
        "<ext>": ext,
        "<name>": name,
        "<shot name>": shot_name,
        "<version name>": version_name,
        "<version>": version
        }

    pattern = resolve_path_tokens(pattern, token_dict)

    translated_path = os.path.join(media_path, pattern) + ".clip"
    print("    Open clip translated path:", translated_path, "\n")

    return translated_path

def create_schematic_reel():
    """Create the destination schematic reel if it doesn't already exist."""

    if SCHEMATIC_REEL not in [reel.name for reel in flame.batch.reels]:
        flame.batch.create_reel(SCHEMATIC_REEL)

def import_open_clip(selection):
    """Resolve and import the open clip for each selected Write File node."""

    for write_node in selection:
        if write_node.type != "Write File":
            continue

        open_clip_path = translate_write_node_path(write_node)

        if not os.path.isfile(open_clip_path):
            message_box("Open clip not found\n\nWrite node export path:\n\n" + open_clip_path)
            continue

        create_schematic_reel()
        flame.batch.import_clip(open_clip_path, SCHEMATIC_REEL)

        print("Open clip imported.")

#-------------------------------------
# [Scopes]
#-------------------------------------

def scope_write_node(selection):

    for item in selection:
        if item.type == "Write File":
            return True
    return False

#-------------------------------------
# [Flame Menus]
#-------------------------------------

def get_batch_custom_ui_actions():

    return [
        {
            "name": "Import...",
            "actions": [
                {
                    "name": "Import Open Clip to Batch",
                    "isVisible": scope_write_node,
                    "execute": import_open_clip,
                    "minimumVersion": "2025"
                }
            ]
        }
    ]
