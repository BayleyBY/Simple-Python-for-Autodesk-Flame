"""
Script Name: SammieRoto Round Trip
Script Version: 1.0
Flame Version: 2026
Written by: Bryan Bayley
Original concept by Wilton Matos. Modified by Bryan Bayley to automate bringing the result back into Flame.
Creation Date: 11.25.25

Description:
- Export selected clips or batch clip nodes as JPEG sequences and automatically open them in Sammie Roto 2.0 for AI-powered rotoscoping.
- After SammieRoto is closed, a dialog asks the user if they want to import the result back into flame.

Menus:
Right-click selected clip(s) in Media Panel -> Export -> Open Sammie 2.0
Right-click Clip Node in Batch -> Export -> Open Sammie 2.0

Requirements:
- JPEG preset (XML) must be at the defined path in the CONFIG below
- Sammie Roto 2.0 installed and configured (see SAMMIE_CMD path below)
- run_sammie.command must forward arguments: python3 launcher.py "$@"

Configuration:
Edit the CONFIG section below to customize:
- SAMMIE_CMD: Path to Sammie Roto 2.0 launcher
- EXPORT_ROOT: Base destination folder for all Sammie exports
- PRESET_PATH: Path to JPEG export preset
- FILE_WAIT_TIMEOUT: Maximum time to wait for export completion

Round Trip Script Updates:
- Build the Export Path using the Flame Project Name and Nickname. This path is specific to Republic Editorial.
- Added function to import the result back into Flame Batch at the cursor position
"""

import os
import re
import time
import subprocess
import flame

# --- PySide6 Imports for Custom Dialog ---
try:
    from PySide6.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
        QApplication, QMessageBox
    )
    from PySide6.QtCore import Qt
    HAS_PYSIDE = True
except ImportError:
    HAS_PYSIDE = False

SCRIPT_NAME = "SammieRoto Round Trip"
FOLDER = "SammieRoto"

# ================== CONFIG ==================
# Sammie-Roto 2.0 launcher path (calls with file argument)
SAMMIE_CMD = ["/bin/bash", "/<YOUR PATH>/Sammie-Roto-2-main/run_sammie.command"]

# JPEG preset path (Shared presets location)
PRESET_PATH = "/<YOUR PATH>/EXPORT_JPEG_SAMMIE.xml"

# Timeout waiting for first frame (seconds):
FILE_WAIT_TIMEOUT = 60

# ============================================


def log(msg):
    print(f"[Sammie Export] {msg}")


def sanitize_filename(name):
    """Replaces invalid filesystem characters with an underscore."""
    # Ensure invalid characters for common file systems are replaced
    return re.sub(r'[<>:"/\\|?*]', "_", name)


def get_current_project_info():
    """
    Retrieves the current Flame project name and nickname (unsanitized strings)
    using the correct API access method: flame.project.current_project.
    Returns: tuple (project_name, project_nickname)
    """
    try:
        current_project = flame.project.current_project

        # Retrieve names as plain strings (no sanitization)
        project_name = str(current_project.name)
        nickname = str(current_project.nickname)

        log(f"Project Info: Name='{project_name}', Nickname='{nickname}'")
        return project_name, nickname
    except Exception as e:
        log(f"Warning: Could not get project info using current_project API: {e}")
        return "Unknown_Project", "No_Nickname"


def get_clip_from_item(item):
    """
    Attempts to retrieve the underlying PyClip or PySequence object
    from a selection item (which might be a PyClip, PySequence, or PyClipNode).
    """
    if isinstance(item, (flame.PyClip, flame.PySequence)):
        return item
    if isinstance(item, flame.PyClipNode):
        for attr in ["clip", "source", "media", "sequence", "input"]:
            val = getattr(item, attr, None)
            if isinstance(val, (flame.PyClip, flame.PySequence)):
                return val

        if hasattr(item, "input_sockets"):
            try:
                for s in item.input_sockets:
                    if hasattr(s, "source") and isinstance(s.source, (flame.PyClip, flame.PySequence)):
                        return s.source
            except Exception as e:
                log(f"Warning: Error checking input sockets: {e}")
                pass

        return item
    return None


def get_sequence_path(clip, subfolder="source"):
    """
    Calculates the full expected path for source or result directory.
    Subfolder should be 'source' or 'result'.
    """
    project_name, nickname = get_current_project_info()
    clip_name_sanitized = sanitize_filename(str(clip.name)[1:-1])

    # Path: /Volumes/<nickname>/<project name>/02_Projects/09_Flame/_sammieroto/
    project_base_path = os.path.join(
        "/Volumes", nickname, project_name,
        "02_Projects", "09_Flame", "_sammieroto"
    )

    # Final Sequence Directory: .../<clip name>/<subfolder>/
    sequence_dir = os.path.join(project_base_path, clip_name_sanitized, subfolder)
    return sequence_dir


def export_clip_to_jpeg_sequence(clip, preset_path):
    """Starts a foreground export job in Flame using the custom path."""
    # Calculate the source directory
    sequence_dir = get_sequence_path(clip, subfolder="source")

    clip_name_sanitized = sanitize_filename(str(clip.name)[1:-1])
    log(f"Exporting clip: {clip_name_sanitized}")
    log(f"Destination folder: {sequence_dir}")

    try:
        # Check and create the full directory path
        if not os.path.exists(sequence_dir):
            os.makedirs(sequence_dir)
            log(f"Created directory: {sequence_dir}")

        if not os.path.exists(preset_path):
            log(f"ERROR: Preset not found at: {preset_path}")
            return None

        exporter = flame.PyExporter()
        exporter.foreground = True  # Blocks the script until export finishes
        log("Export mode: FOREGROUND (waiting for completion)")

        if not hasattr(clip, "name"):
            log("ERROR: Object missing 'name' attribute")
            return None

        exporter.export(clip, preset_path, sequence_dir)
        log("Export command sent and finished (foreground mode)")
        return sequence_dir
    except Exception as e:
        log(f"Error during export: {e}")
        return None


def wait_for_sequence(sequence_dir, timeout=FILE_WAIT_TIMEOUT):
    """
    Waits for the first file to appear in the directory and ensures it has a size > 0.
    """
    log(f"Verifying exported files in: {sequence_dir}")
    start = time.time()

    while time.time() - start < timeout:
        if os.path.exists(sequence_dir):
            # List files and filter for common image extensions
            files = os.listdir(sequence_dir)
            image_files = sorted([
                f for f in files
                if f.lower().endswith((".jpg", ".jpeg", ".tif", ".tiff", ".exr"))
            ])

            if image_files:
                first_frame_name = image_files[0]
                first_frame_path = os.path.join(sequence_dir, first_frame_name)

                # Check for file size > 0 (to ensure it's not a temporary empty file)
                if os.path.getsize(first_frame_path) > 0:
                    log(f"First frame verified: {first_frame_name}")
                    time.sleep(1)
                    return first_frame_path

        time.sleep(0.5)

    log(f"Timeout: No valid image frames created in {timeout}s in {sequence_dir}")
    return None


def open_sequence_in_sammie(first_frame_path):
    """Launches Sammie Roto 2.0 using the configured command."""

    sammie_launcher_path = SAMMIE_CMD[1]
    if not os.path.exists(sammie_launcher_path):
        log(f"ERROR: Sammie Roto launcher not found at: {sammie_launcher_path}")
        return
    if not os.access(sammie_launcher_path, os.X_OK):
        log(f"ERROR: Sammie Roto launcher is not executable: {sammie_launcher_path}")
        return

    try:
        cmd = SAMMIE_CMD + [first_frame_path]
        log(f"Opening sequence in Sammie 2.0 with command: {' '.join(cmd)}")

        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        log("Sammie 2.0 started successfully.")
    except Exception as e:
        log(f"FATAL ERROR: Failed to launch Sammie. Check SAMMIE_CMD configuration. Error: {e}")


def create_batch_result_node(original_node, result_dir):
    """
    Imports the media from result_dir directly into the Batch Schematic Reel
    using the flame.batch.import_clip API with the reel name as a string.
    """
    log(f"Starting auto-import process from: {result_dir}")

    try:
        # 1. Determine Import Path Pattern
        files = sorted([f for f in os.listdir(result_dir) if f.lower().endswith((".exr", ".tif", ".mov", ".mp4", ".mkv", ".jpg", ".jpeg"))])

        if not files:
            log(f"ERROR: No rendered result files found in {result_dir}. Manual import required.")
            return None

        first_file_name = files[0]
        first_file_path = os.path.join(result_dir, first_file_name)
        import_pattern = first_file_path  # Default to first file

        # Try to detect sequence pattern (e.g., filename.0000.ext)
        if len(files) > 1:
            match = re.search(r"\.(\d{4,})\.[^\.]+$", first_file_name)

            if match:
                # Reconstruct the pattern: BaseName + .#### + .Ext
                # match.group(0) includes the preceding dot and the following dot/extension
                parts = first_file_name.rsplit(match.group(0), 1)
                import_pattern = os.path.join(
                    result_dir,
                    f"{parts[0]}.####{match.group(0).replace(match.group(1), '', 1)}"
                )
                log(f"Detected sequence pattern (FINAL): {import_pattern}")
            # If no match, we use the default first_file_path (for single files like .mov)

        # 2. Correct Import to Batch Schematic Reel using the explicit string name
        if hasattr(flame.batch, "import_clip"):

            # Use the explicit reel name provided by the user
            REEL_NAME = "Schematic Reel 1"

            log(f"Importing pattern: {import_pattern} to Reel: {REEL_NAME}")

            # Use the corrected API call with string reel name
            flame.batch.import_clip(import_pattern, REEL_NAME)

            log("Successfully imported clip into Batch Schematic Reel.")
            return True
        else:
            log("ERROR: Required Flame API (flame.batch.import_clip) not found.")
            return False

    except Exception as e:
        log(f"FATAL ERROR during result node creation: {e}")
        return False


def prompt_for_result_import(result_path):
    """
    Custom QDialog to prompt the user and includes a button to copy the result path
    to the system clipboard.
    Returns True if the user clicks 'OK', False otherwise.
    """
    dialog = QDialog()
    dialog.setWindowTitle("Sammie Roto Launched - Save Result Path")
    dialog.setWindowModality(Qt.WindowModal)

    main_layout = QVBoxLayout(dialog)

    # 1. Instructions Label
    main_layout.addWidget(QLabel(
        "Sammie Roto 2.0 has launched successfully.\n\n"
        "**MANUAL STEP:** Please export your roto/matte sequence in Sammie Roto\n"
        "**DIRECTLY TO THE FOLDER BELOW:**"
    ))

    # 2. Copyable Path Field (Non-editable, for display)
    path_display = QLineEdit(result_path)
    path_display.setReadOnly(True)
    path_display.setCursorPosition(0)
    main_layout.addWidget(path_display)

    # 3. Copy Button and Action
    def copy_to_clipboard():
        clipboard = QApplication.clipboard()
        clipboard.setText(result_path)
        QMessageBox.information(
            dialog, "Copied!", "Result path copied to clipboard.", QMessageBox.Ok
        )

    copy_btn = QPushButton("📋 Copy Path to Clipboard")
    copy_btn.clicked.connect(copy_to_clipboard)
    main_layout.addWidget(copy_btn)

    # 4. Final Instruction
    main_layout.addWidget(QLabel(
        "\nClick **OK** when you have saved the result and are ready to automatically import it into Flame."
    ))

    # 5. OK/Cancel Buttons
    button_layout = QHBoxLayout()
    ok_button = QPushButton("OK (Import Now)")
    cancel_button = QPushButton("Cancel Process")

    ok_button.clicked.connect(dialog.accept)
    cancel_button.clicked.connect(dialog.reject)

    button_layout.addWidget(ok_button)
    button_layout.addWidget(cancel_button)
    main_layout.addLayout(button_layout)

    return dialog.exec() == QDialog.Accepted


def export_and_open_sammie(selection):
    log("=" * 60)
    log("STARTING JPEG SEQUENCE EXPORT TO SAMMIE 2.0")
    log("=" * 60)

    # Pre-check for required files
    if not os.path.exists(PRESET_PATH):
        log("ERROR: JPEG preset not found!")
        log(f"Expected location: {PRESET_PATH}")
        return

    sammie_launcher_path = SAMMIE_CMD[1]
    if not os.path.exists(sammie_launcher_path):
        log(f"ERROR: Sammie Roto launcher not found. Check SAMMIE_CMD: {sammie_launcher_path}")
        return

    exported_count = 0
    post_launch_actions = []

    for item in selection:
        clip = get_clip_from_item(item)

        if clip and not isinstance(clip, flame.PyClipNode):
            # 1. Export the clip (to /source/)
            sequence_dir_source = export_clip_to_jpeg_sequence(clip, PRESET_PATH)

            if sequence_dir_source:
                first_frame_path = wait_for_sequence(sequence_dir_source)

                if first_frame_path:
                    # 2. Launch Sammie Roto
                    open_sequence_in_sammie(first_frame_path)
                    exported_count += 1

                    # Store info for post-launch import
                    original_node = item if isinstance(item, flame.PyClipNode) else clip
                    result_dir = get_sequence_path(clip, subfolder="result")

                    post_launch_actions.append({
                        "original_node": original_node,
                        "result_dir": result_dir
                    })
                    log(f"Next step expected result folder: {result_dir}")
                else:
                    log(f"WARNING: Export completed, but no valid frames were verified in: {sequence_dir_source}")
        else:
            log(f"ERROR: Could not extract a valid clip/sequence from item: {type(item).__name__} ({getattr(item, 'name', 'N/A')})")

    log("=" * 60)
    log(f"PROCESS COMPLETED - Exported and launched {exported_count} sequence(s) in Sammie")
    log("=" * 60)

    # --- 3. Handle Post-Launch Import ---
    if post_launch_actions:
        # Prompt user to check Sammie Roto and save result

        QMessageBox.information(
            None,
            "Sammie Roto Launched - Action Required",
            "Sammie Roto 2.0 has launched successfully.\n\n"
            "**MANUAL STEP:** Please export your roto/matte sequence in Sammie Roto\n"
            "**DIRECTLY TO THE FOLLOWING FOLDER:**\n\n"
            f"**{post_launch_actions[0]['result_dir']}**\n\n"
            "Click **OK** when you have saved the result and are ready to automatically import it into Flame.",
            QMessageBox.Ok
        )

        for action in post_launch_actions:
            log("Starting auto-import action...")
            # Ensure the result directory exists before attempting to read from it
            os.makedirs(action["result_dir"], exist_ok=True)

            create_batch_result_node(action["original_node"], action["result_dir"])

    log("=" * 60)
    log("ALL POST-PROCESS ACTIONS COMPLETED")
    log("=" * 60)


def scope_clip(selection):
    return any(isinstance(item, (flame.PyClip, flame.PySequence)) for item in selection)


def scope_clip_node(selection):
    return all(isinstance(item, flame.PyClipNode) for item in selection)


def get_media_panel_custom_ui_actions():
    return [{
        "name": FOLDER,
        "actions": [{
            "name": "Open Sammie 2.0",
            "execute": export_and_open_sammie,
            "minimumVersion": "2022",
        }]
    }]


def get_batch_custom_ui_actions():
    return [{
        "name": FOLDER,
        "actions": [{
            "name": "Open Sammie 2.0",
            "execute": export_and_open_sammie,
            "minimumVersion": "2022",
        }]
    }]


get_media_panel_custom_ui_actions.minimum_version = "2022"
get_batch_custom_ui_actions.minimum_version = "2022"
