# New Project Setup

**Script:** `new_project_setup.py`  
**Version:** 1.0 | **Flame:** 2023+  
**Context:** Media Panel (right-click on Workspace)

## Description

Configurable one-click new-project setup. A community-shareable generalization of a facility-specific project setup script: instead of hard-wired reel layouts and paths, a setup window asks how **your** projects should be laid out and saves the answers. After that, each action — or **All The Things** — runs with your saved settings.

The setup window opens automatically the first time any action is used, and can be reopened anytime via **Setup...** in the same menu.

## Actions

| Action | Description |
|--------|-------------|
| **Clean Desktop** | Deletes all reel groups and batch groups on the desktop, then creates your configured reel group (reels/sequence reels, each with its own colour) and renames/recolours the auto-created batch group. |
| **Clear and Rename Library** | Renames the first library to the project name (or a custom name, or leaves it alone), colours it, and optionally deletes Flame's default "Sequence" stubs. |
| **Create ReelGroup for Online** | Creates your configured online reel group (e.g. `_Sources Sequence` / `Sources` / `Conform`) in the first library. |
| **Create Standard Project Bookmarks** | Copies your saved bookmarks file to `/opt/Autodesk/project/<project>/status/cf_bookmarks.json`. |
| **All The Things** | Runs all four actions in sequence; failures in one step don't stop the rest. |
| **Setup...** | Reopens the setup window to change any of the above. |

## Setup window

Four tabs, one per action:

- **Clean Desktop** — reel group name + colour, batch group name + colour, and an editable list of reels (name, Reel / Sequence Reel, colour — nine presets or a custom picker).
- **Library** — rename-to-project-name toggle (or custom name), library colour, delete-default-sequences toggle.
- **Online Reel Group** — group name + colour and its own editable reel list. (Flame reel groups can only contain reels and sequence reels — folders are not supported inside reel groups.)
- **Bookmarks** — browse to a saved Flame bookmarks `.json`. Tip: set up bookmarks once in any project, then use that project's `status/cf_bookmarks.json` as the template. Leave empty to skip.

Settings are saved as `new_project_setup_config.json` next to the script (shared by everyone loading it from a shared hooks directory); if that location isn't writable, a per-user file in the home directory is used instead.

## Usage

1. Right-click the **Workspace** in the Media Panel.
2. Choose **New Project Setup > All The Things** (or any individual action).
3. First run: fill in the setup window and **Save** — the action then runs with your settings.

## Requirements

- Flame 2023+ (PySide6/PySide2 fallback included)
- Bookmarks action only: a saved bookmarks `.json` and a writable `/opt/Autodesk/project/<project>/status/` directory
