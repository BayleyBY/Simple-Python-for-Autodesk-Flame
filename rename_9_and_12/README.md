# Rename Keep ID

**Script:** `_BB_rename_9_and_12_001.py`  
**Version:** 1.0 | **Flame:** 2020+  
**Context:** Media Panel (right-click on clip)  
**Help from:** John Geehreng

## Description

Renames selected clips by truncating their names to a specific length. Designed for broadcast TVC delivery where ad IDs have strict character-length formats.

## Options

| Action | Length | Use Case |
|--------|--------|----------|
| **Keep 9 (FCB ID)** | 9 characters | FCB-format spot ID |
| **Keep 12 (AD-ID)** | 12 characters | Standard AD-ID format |
| **Remove Last 22** | Removes last 22 chars | Strips suffixes added by Premiere XML fixer tools |

## Usage

1. Select one or more clips in the Media Panel.
2. Right-click → **Rename... > Keep 9 (FCB ID)**, **Keep 12 (AD-ID)**, or **Remove Last 22**

## Requirements

- Flame 2020+
- Selection must contain `PyClip` objects
