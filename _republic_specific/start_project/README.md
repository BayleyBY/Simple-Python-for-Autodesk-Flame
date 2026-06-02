# Start Project

> 🔒 **Workflow-specific — not submitted to the Logik Portal.** This script is hard-wired to a specific facility setup (standard reel/library layout and a shared bookmarks template path), so it is kept here under `_republic_specific/` rather than shared. It still follows the repo's naming and docstring standards so it can be adapted.

**Script:** `start_project.py`  
**Version:** 1.0 | **Flame:** 2024.2.1+  
**Context:** Media Panel (right-click on Workspace)

## Description

A project setup utility that configures a new Flame project to a standard layout in one click. Accessed by right-clicking on the **Workspace** in the Media Panel.

## Individual Actions

| Action | Description |
|--------|-------------|
| **Clean Desktop** | Deletes all existing reel groups and batch groups. Creates a single "Reels" reel group (green) with Reel1/Reel2/Reel3. Renames the auto-created Batch group to "Batch" (blue). |
| **Clear and Rename Library** | Renames the default library to match the project name and colors it red `(96, 12, 12)`. Deletes any auto-created Sequence stubs. |
| **Create ReelGroup for Online** | Creates an "Online Assemble" reel group in the first library with `_Sources Sequence`, `Sources`, and `Conform` reels (same structure as the standalone `create_reel_group` script). |
| **Create Standard Project Bookmarks** | Copies a standard `cf_bookmarks.xml` template from a shared location to the project's status directory at `/opt/Autodesk/project/<ProjectName>/status/`. |
| **All The Things** | Runs all four actions above in sequence. |

## Path Assumptions

- Bookmark template lives at: `/Volumes/Flame_Archive/_discreet/_bookmarks_standard_project/cf_bookmarks.xml`

## Usage

1. Right-click on the **Workspace** in the Media Panel.
2. Select **New Project Setup > All The Things** (or any individual action).

## Requirements

- Flame 2024.2.1+
- Bookmark template file present at the path above
