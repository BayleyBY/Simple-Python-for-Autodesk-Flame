# Set In Out

> 🔒 **Workflow-specific — not submitted to the Logik Portal.** The presets hard-code a specific facility's slate/picture timecode layout and delivery workflows (including a "Republic Master" preset), so it is kept here under `republic_specific/` rather than shared. It still follows the repo's naming and docstring standards so it can be adapted.

**Script:** `set_in_out.py`  
**Version:** 1.0 | **Flame:** 2021.1+  
**Context:** Media Panel (right-click on clip)

## Description

Sets In/Out marks on selected clips for various delivery and approval workflows. All presets assume a standard sequence layout:

- **Slate at:** `59:53:00`
- **First frame of picture at:** `1:00:00:00`
- **1 second of black at the end of the sequence**
- Frame rate: 23.98/24

## Presets

| Action | In Point | Out Point | Use Case |
|--------|----------|-----------|----------|
| **Clear All In-Out** | None | None | Reset |
| **Client Posting** | `59:59:00` | Last frame + 1 | No slate, no tail black |
| **Slated Approvals** | `59:53:00` | Last frame + 1 | Slate with full tail black |
| **Slated Delivery** | `59:53:00` | Last frame − 23 | Slate, tail black trimmed off |
| **OLV/Social** | `1:00:00:00` | Last frame − 23 | No slate, no tail black |
| **Republic Master** | `59:51:00` | Last frame + 1 | 2-second head / slate / full tail |

## Usage

1. Select one or more clips in the Media Panel.
2. Right-click → **Set In-Out... > [desired preset]**

## Requirements

- Flame 2022+
- Selection must contain `PyClip` objects
