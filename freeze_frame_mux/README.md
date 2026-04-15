# Freeze Frame Mux

**Script:** `_BB_freeze_frame_mux_001.py`  
**Version:** 1.0 | **Flame:** 2021.1+  
**Context:** Batch (right-click on any node)

## Description

Adds a **Mux** node after the currently selected node and configures it to freeze on the current frame. Useful for holding a frame while keeping the rest of the batch network intact.

The Mux is configured as follows:

- Positioned 200 units to the right of the source node
- Assigned the next available context slot
- `range_active = True` with both start and end set to the current playhead frame
- `before_range` = **Repeat First**, `after_range` = **Repeat Last**
- Connected to the source node's default output
- If the source node has a matte/alpha output socket, it is connected to `Matte_0`

## Usage

1. In Batch, right-click on any node.
2. Select **Batch Nodes... > Add Mux and Freeze**

## Requirements

- Selection must contain `PyNode` objects in Batch
