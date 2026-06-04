# import_open_clip.py — working notes

Origin: a stripped fork of *Import Write Node* (Michael Vaglienty), Logik Portal
snapshot `26-03-03`, v2.11.0 — kept only the **Import Open Clip to Batch** action
and added Flame 2027 token handling. The original full script lives at
`/Volumes/Flame_Archive/_python/_LOGIK/LogikPortal_Snapshot_26-03-03/python-main/import_write_node/`.

This copy is now a **single self-contained `.py` file** — the PyFlame library and
`config/` dependencies have been inlined/removed (see "Self-contained rewrite").

## Deploy

Single file — copy `import_open_clip.py` into Flame's Python path and rescan
Python hooks (or restart). No `lib/` or `config/` folder needed. Syntax check
first: `python3 -c "import ast; ast.parse(open('import_open_clip.py').read())"`.

## Self-contained rewrite

The script originally did `from lib.pyflame_lib_import_open_clip import *` and read
`config/config.json`. Both dependencies were removed:

| was (PyFlame) | now |
|---------------|-----|
| `pyflame.print_title` / `pyflame.print` | plain `print()` |
| `pyflame.verify_script_install` | dropped (only relevant to multi-file installs) |
| `PyFlameConfig` + `config/config.json` | `SCHEMATIC_REEL` module constant |
| `PyFlameMessageWindow` / `MessageType` | `message_box()` via QtWidgets (PySide6→PySide2) |

The `ImportWriteNode` class was flattened to module-level functions:
`get_batch_custom_ui_actions` → `import_open_clip` → `translate_write_node_path`
(+ `resolve_path_tokens`/`apply_token_slice`) → `create_schematic_reel` →
`flame.batch.import_clip`. `scope_write_node` = visibility.

The earlier fork also **removed** (unused by this action): `setup()` UI +
`get_main_menu_custom_ui_actions`; the Renders Reel action; post-render
auto-import (`post_render_import` + `batch_export_end`); all config keys except
`schematic_reel`.

## Bugs fixed (in order found)

1. **Token slicing (Flame 2027).** Tokens can carry a slice suffix, e.g.
   `<shot name[0:-6]>`, `<source name[9:15]>`. The original exact-string
   `pattern.replace('<shot name>', value)` never matched sliced tokens and left
   them literal. Replaced with `resolve_path_tokens()` (regex, longest-name-first
   so `<batch name>` beats `<name>`) + `apply_token_slice()` (Python slicing
   matches Flame's documented semantics: 0-based front / -1 end, start inclusive,
   stop exclusive, clamped). The only token Flame won't slice is `<extension>`.
2. **Literal quotes.** `str(flame.batch.current_iteration.name)` (no strip)
   leaked `'...'` into paths. All Flame string `PyAttribute`s' `str()` are
   quote-wrapped → use `[1:-1]` (as the sibling reads already did).
3. **`<version name>`** was wrongly mapped to the batch iteration name. It's the
   write node's own `version_name` (e.g. `comp`).
4. **`<version>`** was a hardcoded `zfill(3)` guess. It's `version_number`
   zero-padded to the node's `version_padding`.

## Token → source mapping (current)

| token            | source                                                        | notes |
|------------------|---------------------------------------------------------------|-------|
| `<project>`      | `flame.project.current_project.name`                          | plain str, no `[1:-1]` |
| `<project nickname>` | `flame.project.current_project.nickname`                  | plain str |
| `<batch iteration>` | `flame.batch.current_iteration.name` `[1:-1]`              | iteration name |
| `<batch name>`   | `flame.batch.name` `[1:-1]`                                    | |
| `<ext>`          | `''`                                                          | hardcoded empty (was `format_extension`) |
| `<name>`         | `write_node.name` `[1:-1]`                                     | schematic node name, e.g. `ns_sh220_v002` |
| `<shot name>`    | `write_node.shot_name` `[1:-1]`                               | |
| `<version name>` | `write_node.version_name` `[1:-1]`                            | e.g. `comp` |
| `<version>`      | `str(write_node.version_number).zfill(int(str(write_node.version_padding)))` | e.g. `002` |

## Key API facts (from a diagnostic probe of a live write node)

- Write node version attrs: `version_name` (string, quoted), `version_number`
  (int), `version_padding` (int), `version_mode` (e.g. `'Follow Iteration'`).
- `write_node.get_resolved_media_path()` returns the **fully Flame-resolved**
  image path — the ground-truth way to confirm what a token resolves to, e.g.
  `.../ns_sh220_comp_v002/ns_sh220_comp_002.[001-054].exr`.
- `write_node.attributes` returns the full attribute-name list.
- `media_path` is delivered already token-resolved by Flame; only
  `create_clip_path` still contains tokens, which this script resolves itself.

## Worked example (real shot)

Pattern: `<project nickname>/<project>/02_Projects/09_Flame/_publish/<shot name[0:-6]>/<shot name>/_open_clip/<shot name>_<version name>`
→ `/Volumes/Republic_2026_Q2/R2604-952_NatureSweet/02_Projects/09_Flame/_publish/ns/ns_sh220/_open_clip/ns_sh220_comp.clip`
(`<shot name>`=`ns_sh220`, `[0:-6]`=`ns`, `<version name>`=`comp`).

## Gotcha

`<version name>` ≠ `<name>` ≠ `<batch iteration>` — in this facility's template
the node name is `<shot>_v<ver>` while the version name is the task (`comp`).
Always verify token meaning against `get_resolved_media_path()`, don't assume.
```
