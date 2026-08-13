"""
Script Name: Move Playhead
Script Version: 2.0
Flame Version: 2025
Written by: Bryan Bayley
Creation Date: 08.05.26
Update Date: 08.13.26

Description:
Moves the playhead (positioner) of all selected clips or sequences to an
absolute record timecode. The timecodes offered in the menu are yours to
set — Setup... opens a window where you add, label, reorder and remove as
many as you need, and each one becomes its own menu action alongside the
Setup option. Settings are saved to a JSON file next to the script, so the
menu comes back the same way in every project.

The playhead can be parked before the first frame of the sequence (e.g.
00:59:53:00 on a sequence whose record starts at 01:00:00:00), which is
useful for preparing slate insertions and other head work at standard
broadcast lead-in positions.

Menus:
Right-click selected clips or sequences in the Media Panel -> Move Playhead... -> Move Playhead to <your timecode>
Right-click selected clips or sequences in the Media Panel -> Move Playhead... -> Move Playhead to Custom Timecode
Right-click selected clips or sequences in the Media Panel -> Move Playhead... -> Setup...

Updates:
v2.0 08.13.26
- The menu timecodes are now user-configurable: Setup... adds, labels,
  reorders and removes them, and each becomes its own menu action.
- Settings are saved to move_playhead_config.json next to the script
  (falling back to the home directory when that is not writable).
- Timecodes can carry an optional label, shown as "Move Playhead to
  Slate (00:59:53:00)".
- The Custom Timecode action can be hidden from the menu.
- The original 00:59:53:00 and 01:00:00:00 presets ship as the defaults,
  so the menu is unchanged until it is edited.
"""

import json
import os
import re
import traceback

import flame

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

SCRIPT_NAME = "Move Playhead"
FOLDER = "Move Playhead..."
CONFIG_FILE_NAME = "move_playhead_config.json"

TIMECODE_PATTERN = re.compile(r"^\d{1,2}:\d{2}:\d{2}[:;]\d{1,2}$")

DEFAULT_CONFIG = {
    "timecodes": [
        {"label": "", "timecode": "00:59:53:00"},
        {"label": "", "timecode": "01:00:00:00"},
    ],
    "show_custom": True,
}


def message_box(message):

    mbox = QtWidgets.QMessageBox()
    mbox.setWindowTitle(SCRIPT_NAME)
    mbox.setText(message)
    mbox.exec()


# ---------------------------------------------------------------- settings --

def config_paths():
    # Preferred location is next to the script (shared with everyone loading
    # it); the home directory is the fallback when that is not writable.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return [
        os.path.join(script_dir, CONFIG_FILE_NAME),
        os.path.join(os.path.expanduser("~"), "." + CONFIG_FILE_NAME),
    ]


def clean_timecodes(entries):
    # The config file is hand-editable, so never trust its shape: drop
    # anything that would not build a valid menu action.
    cleaned = []
    if not isinstance(entries, list):
        return cleaned
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        timecode = str(entry.get("timecode", "")).strip()
        if not TIMECODE_PATTERN.match(timecode):
            continue
        cleaned.append({
            "label": str(entry.get("label", "")).strip(),
            "timecode": timecode,
        })
    return cleaned


def clean_config(config):
    if not isinstance(config, dict):
        return dict(DEFAULT_CONFIG)
    return {
        "timecodes": clean_timecodes(config.get("timecodes")),
        "show_custom": bool(config.get("show_custom", True)),
    }


def load_config():
    for path in config_paths():
        if os.path.isfile(path):
            try:
                with open(path) as config_file:
                    return clean_config(json.load(config_file))
            except (OSError, ValueError):
                traceback.print_exc()
    return None


def save_config(config):
    for path in config_paths():
        try:
            with open(path, "w") as config_file:
                json.dump(config, config_file, indent=4)
        except OSError:
            traceback.print_exc()
            continue
        print("%s: settings saved to %s" % (SCRIPT_NAME, path))
        return True
    message_box("Could not save settings — see shell for details.")
    return False


def active_config():
    config = load_config()
    if config is None or not config["timecodes"] and not config["show_custom"]:
        return DEFAULT_CONFIG
    return config


# ---------------------------------------------------------------- setup UI --

class TimecodeListEditor(QtWidgets.QWidget):
    """Editable list of menu timecodes: timecode, optional label, order."""

    def __init__(self, timecodes):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QtWidgets.QHBoxLayout()
        timecode_header = QtWidgets.QLabel("Timecode")
        timecode_header.setFixedWidth(140)
        header.addWidget(timecode_header)
        header.addWidget(QtWidgets.QLabel("Label (optional)"))
        header.addSpacing(96)
        layout.addLayout(header)

        self.rows = []
        self.rows_layout = QtWidgets.QVBoxLayout()
        layout.addLayout(self.rows_layout)

        add_button = QtWidgets.QPushButton("Add Timecode")
        add_button.clicked.connect(lambda: self.add_row())
        layout.addWidget(add_button)

        for entry in timecodes:
            self.add_row(entry)

    def add_row(self, entry=None):
        if entry is None:
            entry = {"label": "", "timecode": ""}

        row = QtWidgets.QWidget()
        row_layout = QtWidgets.QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        timecode_edit = QtWidgets.QLineEdit(entry["timecode"])
        timecode_edit.setPlaceholderText("HH:MM:SS:FF")
        timecode_edit.setFixedWidth(140)
        label_edit = QtWidgets.QLineEdit(entry["label"])
        label_edit.setPlaceholderText("e.g. Slate — shown before the timecode")

        up_button = QtWidgets.QPushButton("▲")
        up_button.setFixedWidth(28)
        down_button = QtWidgets.QPushButton("▼")
        down_button.setFixedWidth(28)
        remove_button = QtWidgets.QPushButton("✕")
        remove_button.setFixedWidth(28)

        row_layout.addWidget(timecode_edit)
        row_layout.addWidget(label_edit)
        row_layout.addWidget(up_button)
        row_layout.addWidget(down_button)
        row_layout.addWidget(remove_button)

        row_entry = (row, timecode_edit, label_edit)
        self.rows.append(row_entry)
        up_button.clicked.connect(lambda: self.move_row(row_entry, -1))
        down_button.clicked.connect(lambda: self.move_row(row_entry, 1))
        remove_button.clicked.connect(lambda: self.remove_row(row_entry))
        self.rows_layout.addWidget(row)

    def move_row(self, row_entry, offset):
        index = self.rows.index(row_entry)
        new_index = index + offset
        if new_index < 0 or new_index >= len(self.rows):
            return
        self.rows.pop(index)
        self.rows.insert(new_index, row_entry)
        row = row_entry[0]
        self.rows_layout.removeWidget(row)
        self.rows_layout.insertWidget(new_index, row)

    def remove_row(self, row_entry):
        self.rows.remove(row_entry)
        row = row_entry[0]
        row.setParent(None)
        row.deleteLater()

    def timecode_configs(self):
        # Rows are kept in menu order; empty rows are dropped.
        entries = []
        for row, timecode_edit, label_edit in self.rows:
            timecode = timecode_edit.text().strip()
            if not timecode:
                continue
            entries.append({
                "label": label_edit.text().strip(),
                "timecode": timecode,
            })
        return entries


class SetupDialog(QtWidgets.QDialog):

    def __init__(self, config):
        super().__init__()
        self.setWindowTitle("%s — Setup" % SCRIPT_NAME)
        self.setMinimumWidth(620)
        layout = QtWidgets.QVBoxLayout(self)

        intro = QtWidgets.QLabel(
            "Each timecode below becomes its own action in the "
            "\"%s\" menu, in this order." % FOLDER)
        intro.setWordWrap(True)
        layout.addWidget(intro)

        self.timecodes = TimecodeListEditor(config["timecodes"])
        layout.addWidget(self.timecodes)

        self.show_custom = QtWidgets.QCheckBox(
            "Show \"Move Playhead to Custom Timecode\" in the menu")
        self.show_custom.setChecked(config["show_custom"])
        layout.addWidget(self.show_custom)

        note = QtWidgets.QLabel(
            "Timecodes are absolute record timecodes, written as HH:MM:SS:FF "
            "(a semicolon before the frames marks drop frame). A timecode "
            "before the start of a sequence is fine — the playhead parks "
            "there without clamping.")
        note.setWordWrap(True)
        layout.addWidget(note)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept(self):
        entries = self.timecodes.timecode_configs()

        invalid = [entry["timecode"] for entry in entries
                   if not TIMECODE_PATTERN.match(entry["timecode"])]
        if invalid:
            message_box("These are not valid timecodes:\n\n%s\n\nUse "
                        "HH:MM:SS:FF, e.g. 00:59:53:00."
                        % "\n".join(invalid))
            return

        seen = []
        duplicates = []
        for entry in entries:
            if entry["timecode"] in seen:
                duplicates.append(entry["timecode"])
            else:
                seen.append(entry["timecode"])
        if duplicates:
            message_box("Each timecode can only appear once in the menu.\n\n"
                        "Listed more than once:\n\n%s" % "\n".join(duplicates))
            return

        if not entries and not self.show_custom.isChecked():
            message_box("Add at least one timecode, or keep the Custom "
                        "Timecode action — otherwise the menu would have "
                        "nothing to run.")
            return

        super().accept()

    def result_config(self):
        return {
            "timecodes": self.timecodes.timecode_configs(),
            "show_custom": self.show_custom.isChecked(),
        }


def refresh_menus():
    # The menu is built from the config, so it has to be rebuilt after a
    # save. Flame's own rescan does this without restarting.
    try:
        flame.execute_shortcut("Rescan Python Hooks")
        return True
    except Exception:
        traceback.print_exc()
        return False


def run_setup():
    dialog = SetupDialog(active_config())
    if dialog.exec() != QtWidgets.QDialog.Accepted:
        return
    config = dialog.result_config()
    if not save_config(config):
        return
    if not refresh_menus():
        message_box("Settings saved.\n\nThe menu updates after Flame rescans "
                    "its Python hooks (Flame menu -> Rescan Python Hooks).")


# ----------------------------------------------------------------- actions --

def move_playhead(selection, target_timecode):

    print("--- Move Playhead to %s ---" % target_timecode)
    failed = []

    for clip in selection:
        if not isinstance(clip, flame.PyClip):
            continue
        clip_name = str(clip.name)[1:-1]
        try:
            clip.current_time = flame.PyTime(target_timecode, clip.frame_rate)
            print("%s: playhead moved to %s" % (clip_name, target_timecode))
        except Exception:
            traceback.print_exc()
            failed.append(clip_name)

    if failed:
        message_box(
            "Could not move the playhead on:\n\n%s\n\nSee the shell for details."
            % "\n".join(failed))


def make_move_action(target_timecode):
    # Built per menu entry so each action keeps its own timecode.
    def execute(selection):
        move_playhead(selection, target_timecode)
    return execute


def move_playhead_custom(selection):

    timecode, ok = QtWidgets.QInputDialog.getText(
        None, SCRIPT_NAME, "Timecode (HH:MM:SS:FF):", text="01:00:00:00")
    if not ok:
        return

    timecode = timecode.strip()
    if not TIMECODE_PATTERN.match(timecode):
        message_box(
            "\"%s\" is not a valid timecode.\n\nUse HH:MM:SS:FF, e.g. 00:59:53:00."
            % timecode)
        return

    move_playhead(selection, timecode)


def open_setup(selection):

    run_setup()


def scope_clip(selection):

    for item in selection:
        if isinstance(item, flame.PyClip):
            return True
    return False


def action_name(entry):
    if entry["label"]:
        return "Move Playhead to %s (%s)" % (entry["label"], entry["timecode"])
    return "Move Playhead to %s" % entry["timecode"]


def get_media_panel_custom_ui_actions():

    config = active_config()
    actions = []

    for entry in config["timecodes"]:
        actions.append({
            "name": action_name(entry),
            "isVisible": scope_clip,
            "execute": make_move_action(entry["timecode"])
        })

    if config["show_custom"]:
        actions.append({
            "name": "Move Playhead to Custom Timecode",
            "isVisible": scope_clip,
            "execute": move_playhead_custom
        })

    actions.append({
        "name": "Setup...",
        "isVisible": scope_clip,
        "execute": open_setup
    })

    return [{
        "name": FOLDER,
        "actions": actions
    }]
