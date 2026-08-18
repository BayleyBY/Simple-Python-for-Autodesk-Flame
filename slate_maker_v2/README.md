# Slate Maker

**Script:** `slate_maker_v2.py`  
**Version:** 2.6.0 | **Flame:** 2027  
**Context:** Media Panel (right-click on slate background clips, slate clips, or sequences)  
**Licence:** GNU General Public License v3.0 — see [`LICENSE`](LICENSE)

> Original *Slate Maker* by **Michael Vaglienty** (v1.0.0, derived from Uber Slate Maker).
> Everything from **v2.0.0 onward was added in-house by Bryan Bayley**, with the original
> author's permission. Distributed under the GPL-3.0 it was published under.

## Description

Creates slates from CSV data using Type Node templates, and updates them after the fact.
Slates of multiple ratios can be built from one CSV, text can be previewed before creation,
clips are auto-named from tokens, and token values (date, copyright, agency…) can be
bulk-edited later across a whole selection.

Does not work with Flare. Legacy Text Node templates are not supported.

## Menus

Flame's menu API has no nested subfolders, so the update tools get a sibling folder:

```
Slate Maker...         -> Create Slates              (select slate background clip(s))
Slate Maker...         -> Rename from Slate          (sequences containing a slate, or slate clips)
Slate Maker: Update... -> Update Slates              (bulk editor)
Slate Maker: Update... -> Update <Field>             (one item per learned field; works on any slate)
Slate Maker: Update... -> Edit Update Fields         (curate the Update <Field> list)
```

## What v2 added

- **Update Slates** — token values are stamped at creation and can be bulk-edited later.
- **Rename from Slate** — renames sequences/clips from their slate tokens via a pattern such as `<AD-ID>_<TITLE>`.
- **Per-field updates** — one menu item per field, so a single value can be changed across a whole selection. Works on *any* slate, including ones this script did not create, by matching the field's label line in the Type Node text.
- **Metadata stamping** (v2.5.0+, Flame 2027) — slate metadata lives on a `Source Metadata` TimelineFX on the slate segment via the PyMetadataNode API, so it travels with the clip into sequences. Slates from v2.0.0–v2.4.x used clip tags and are still read and updated through them.
- **Learned update fields** (v2.6.0) — the field list populates itself from the tokens of each creation run, so the menu is facility-agnostic rather than hard-coded.

See the `Version History:` block in the script header for per-version detail.

## Usage

1. Point the script at a CSV whose first-row column headers are the token names, in **all caps**.
2. Build a Type Node template using those tokens, also in all caps. Put each line of the slate on its own layer if you want the preview to be accurate.
3. Select the slate background clip(s) in the Media Panel and run **Slate Maker... > Create Slates**.

For multi-ratio output the CSV needs a `RATIO` column, and only the ratios matching the selected backgrounds are created. With a single background and no `RATIO` column, every CSV row produces a slate.

Working examples (CSVs, backgrounds and templates for both single and multi-ratio setups) are in [`example_files/`](example_files/).

## Installation

This is a **multi-file script** — copy the whole `slate_maker_v2/` folder, not just the `.py`:

```
/opt/Autodesk/shared/python/
```

At this facility it is deployed to `/Volumes/Flame_Archive/SHARED/python/BB_python/slate_maker_v2/`.

## Requirements

- Flame 2027 (the metadata stamping uses the PyMetadataNode API; v2.5.0+ requires it)
- `lib/pyflame_lib_slate_maker_v2.py` — bundled, GPL-3.0, by Michael Vaglienty
- `assets/fonts/` — Montserrat, used by the UI

## Notes

- `config/config.json` is **not** tracked in this repo — it holds machine-local paths written at runtime. The script recreates it from `DEFAULT_CONFIG` on first use.
- Tokens in both the Type Node template and the CSV headers must be in all caps.
- If a sequence contains multiple slate segments, only the first is updated.
- Slates created by v1.0.0 carry no stamped metadata and cannot be bulk-updated, though per-field updates still work on them via label-line matching.
