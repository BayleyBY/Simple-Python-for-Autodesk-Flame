# Update Slate Date

**Script:** `_BB_update_slate_date_005.py`  
**Version:** 1.5 | **Flame:** 2021+  
**Context:** Media Panel (right-click on sequence)  
**Help from:** Fred Warren, Philippe Jean

## Description

Updates all **Burn-in Metadata** timeline effects in selected sequences to show the current date. Designed for refreshing slate dates before a new round of deliveries.

The script walks every segment in every track of each selected sequence, finds segments with a `Burn-in Metadata` effect, selects that segment, and fires the `Update` shortcut to refresh the date field.

## Prerequisites

This script relies on `flame.execute_shortcut("Update")`, which requires a custom shortcut to be registered for the **Update** button in the Burn-in Metadata Layer Specific menu:

1. Open a sequence with a Burn-in Metadata effect.
2. Open the **Layer Specific** menu for that effect.
3. Assign any key to the **Update** button — then clear the key if you don't want it mapped. The shortcut entry just needs to exist.

Additionally:
- The Burn-in Metadata effect must be on a segment or gap segment **with no other soft effects**.
- Before running the script, ensure the **Layer Specific** menu for a Burn-in Metadata segment is visible on the first sequence.

## Usage

1. Select one or more sequences in the Media Panel.
2. Right-click → **Slates... > Update Slate Date**

## Requirements

- Flame 2021+
- "Update" shortcut registered for Burn-in Metadata Layer Specific menu
- Selection must contain `PySequence` objects
