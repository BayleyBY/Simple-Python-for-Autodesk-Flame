# SammieRoto Round Trip

> 🔒 **Workflow-specific — not submitted to the Logik Portal.** Hard-wired to a Republic Editorial path layout, a local Sammie Roto 2.0 install, and a named JPEG export preset. Kept here under `_republic_specific/`. It still follows the repo's naming and docstring standards so it can be adapted — edit the `CONFIG` block before use.

**Script:** `sammieroto_round_trip.py`  
**Version:** 1.0 | **Flame:** 2026+  
**Context:** Media Panel / Batch (right-click on clips or a clip node)  
**Original concept:** Wilton Matos | **Round-trip automation:** Bryan Bayley

## Description

Exports selected clips (or batch clip nodes) as JPEG sequences and opens them in [Sammie Roto 2.0](https://github.com/) for AI-powered rotoscoping. After you export the result out of Sammie Roto into the indicated folder, the script imports it back into the Flame Batch Schematic Reel.

## What it does

1. Exports each selected clip to a per-clip `source/` folder as a JPEG sequence (foreground export).
2. Waits for the first valid frame, then launches Sammie Roto 2.0 on it.
3. Prompts you to export your roto/matte result into the matching `result/` folder.
4. Imports the result sequence back into the Batch Schematic Reel.

Export path layout: `/Volumes/<nickname>/<project>/02_Projects/09_Flame/_sammieroto/<clip>/{source,result}/`

## Configuration

Edit the `CONFIG` block at the top of the script before first use:

- `SAMMIE_CMD` — path to the Sammie Roto 2.0 `run_sammie.command` launcher
- `PRESET_PATH` — path to the JPEG export preset (`EXPORT_JPEG_SAMMIE.xml`, bundled in this folder)
- `FILE_WAIT_TIMEOUT` — seconds to wait for the first exported frame

## Usage

1. Select clip(s) in the Media Panel, or a clip node in Batch.
2. Right-click → **SammieRoto > Open Sammie 2.0**

## Requirements

- Flame 2026+
- PySide6 (bundled with Flame 2026)
- Sammie Roto 2.0 installed; `run_sammie.command` must forward args (`python3 launcher.py "$@"`)
- JPEG export preset installed at the `PRESET_PATH` you configure
- Facilis storage mounted at `/Volumes`; project nickname = partition, project name = job folder
