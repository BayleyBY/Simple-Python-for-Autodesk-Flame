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

from lib.pyflame_lib_import_open_clip import *

#-------------------------------------
# [Constants]
#-------------------------------------

SCRIPT_NAME = 'Import Open Clip to Batch'
SCRIPT_VERSION = 'v1.00.0'
SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))

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
    bounds = inner.split(':')

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
        r'<(' + '|'.join(re.escape(name) for name in names) + r')(\[[^\]]*\])?>'
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

class ImportWriteNode:

    def __init__(self, selection):

        pyflame.print_title(f'{SCRIPT_NAME} {SCRIPT_VERSION}')

        # Check script path, if path is incorrect, stop script.
        if not pyflame.verify_script_install():
            return

        self.selection = selection

        # Create/Load config file settings.
        self.settings = self.load_config()

    def load_config(self) -> PyFlameConfig:
        """
        Load Config
        ===========

        Load the destination schematic reel name from the config file, creating
        it with the default if it doesn't exist.
        """

        settings = PyFlameConfig(
             config_values={
                'schematic_reel': 'Renders',
                }
            )

        return settings

    def translate_write_node_path(self):

        print ('Translating write node path...')

        # Translate write node tokens
        for self.write_node in self.selection:
            media_path = str(self.write_node.media_path)[1:-1]
            print ('    media path:', media_path)
            pattern = str(self.write_node.create_clip_path)[1:-1]
            print ('    pattern:', pattern)
            project = str(flame.project.current_project.name)
            project_nickname = str(flame.project.current_project.nickname)
            batch_iteration = str(flame.batch.current_iteration.name)[1:-1]
            batch_name = str(flame.batch.name)[1:-1]
            #ext = str(self.write_node.format_extension)[1:-1]
            ext = ''
            name = str(self.write_node.name)[1:-1]
            shot_name = str(self.write_node.shot_name)[1:-1]
            # <version name> and <version> come from the write node's own
            # versioning so they honour its Version Mode and Padding settings.
            # version_name is a string attr (quote-wrapped); version_number and
            # version_padding are ints. e.g. 'comp', 2, 3 -> 'comp' and '002'.
            version_name = str(self.write_node.version_name)[1:-1]
            version_padding = int(str(self.write_node.version_padding))
            version = str(self.write_node.version_number).zfill(version_padding)

            token_dict = {
                '<project>': project,
                '<project nickname>': project_nickname,
                '<batch iteration>': batch_iteration,
                '<batch name>': batch_name,
                '<ext>': ext,
                '<name>': name,
                '<shot name>':shot_name,
                '<version name>': version_name,
                '<version>': version
                }

            pattern = resolve_path_tokens(pattern, token_dict)

            translated_path = os.path.join(media_path, pattern) + '.clip'
            print ('    Open clip translated path:', translated_path, '\n')

            return translated_path

    def import_to_schematic_reel(self):
        """
        Import To Schematic Reel
        ========================

        Import open clip to batch schematic reel.
        """

        open_clip_path = self.translate_write_node_path()

        if not os.path.isfile(open_clip_path):
            PyFlameMessageWindow(
                message='Open clip not found\n\nWrite node export path:\n\n' + open_clip_path,
                message_type=MessageType.ERROR,
                parent=None,
                )
            return

        self.create_schematic_reel()

        self.import_schematic_reel(open_clip_path)

    def create_schematic_reel(self):
        """
        Create Schematic Reel
        =====================

        Create open clip schematic reel if it doesn't exist.
        """

        if self.settings.schematic_reel not in [reel.name for reel in flame.batch.reels]:
            self.schematic_reel_for_import = flame.batch.create_reel(self.settings.schematic_reel)
        else:
            self.schematic_reel_for_import = [reel for reel in flame.batch.reels if reel.name == self.settings.schematic_reel][0]

    def import_schematic_reel(self, path):
        """
        Import Schematic Reel
        =====================

        Import to schematic reel.
        """

        flame.batch.import_clip(path, self.settings.schematic_reel)

#-------------------------------------

def schematic_import(selection):

    script = ImportWriteNode(selection)
    script.import_to_schematic_reel()

    pyflame.print('Open clip imported.', text_color=TextColor.GREEN)

#-------------------------------------
# [Scopes]
#-------------------------------------

def scope_write_node(selection):

    for item in selection:
        if item.type == 'Write File':
            return True
    return False

#-------------------------------------
# [Flame Menus]
#-------------------------------------

def get_batch_custom_ui_actions():

    return [
        {
            'name': 'Import...',
            'actions': [
                {
                    'name': 'Import Open Clip to Batch',
                    'isVisible': scope_write_node,
                    'execute': schematic_import,
                    'minimumVersion': '2025'
                }
            ]
        }
    ]
