# Cache Motion Vectors

**Script:** `_BB_cache_motion_vectors_001.py`  
**Version:** 1.1 | **Flame:** 2021.1+  
**Context:** Batch (right-click on a Clip node)

## Description

A simplified batch utility that automatically builds the node network needed to cache motion vectors for a selected clip.

When run, it:
1. Creates an **Action** node to the right of the selected clip.
2. Creates a **Media** node between the clip and the Action node.
3. Connects the clip → Media → Action.
4. Creates a **Motion Vectors Map** node inside the Action.
5. Caches motion vectors across the full clip duration.

## Usage

1. In Batch, right-click on a **Clip** node.
2. Select **Cache... > Cache Motion Vectors**

## Notes

- Only appears on Clip-type nodes in Batch.
- This is a simplified version of the Autodesk example script — desktop functionality has been removed.
