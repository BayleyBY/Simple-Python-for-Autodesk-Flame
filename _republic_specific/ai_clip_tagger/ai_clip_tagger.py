"""
Script Name: AI Clip Tagger
Script Version: 1.0
Flame Version: 2026.2
Written by: Bryan Bayley
Creation Date: 02.24.26

Description:
Tag selected clips with AI-generated scene labels. Exports a single still frame
from each clip, sends it to the Claude vision API, and applies the returned
descriptive tags (person, interior, office, food, etc.) using Flame's native
tag system (clip.tags).

Requires an Anthropic API key saved as plain text at: ~/.anthropic_api_key

Menus:
Right-click clips in the Media Panel -> AI... -> Tag Clips with AI
"""

import flame
import os
import glob
import json
import base64
import urllib.request
import urllib.error
import traceback
import re

SCRIPT_NAME = "AI Clip Tagger"
FOLDER = "AI..."

LOG_PATH = os.path.expanduser("~/Desktop/ai_tagger_log.txt")  # overridden at runtime

# Haiku pricing — update if Anthropic changes rates
COST_PER_INPUT_TOKEN  = 0.80 / 1_000_000
COST_PER_OUTPUT_TOKEN = 4.00 / 1_000_000


def log(msg):
    flame.messages.show_in_console(f"AI Tagger: {msg}", "info")
    with open(LOG_PATH, "a") as f:
        f.write(msg + "\n")


# ── Config ────────────────────────────────────────────────────────────────────
API_KEY_PATH    = os.path.expanduser("~/.anthropic_api_key")
JPG_PRESET_PATH = "/Volumes/Flame_Archive/SHARED/export/presets/file_sequence/JPG View Baked.xml"
CLAUDE_MODEL    = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = (
    "You are a visual content tagging assistant. "
    "Analyze the image and return a JSON array of short, lowercase descriptive tags. "
    "Include tags for: people (person, man, woman, child, group), "
    "environment (interior, exterior), setting (office, home, kitchen, restaurant, "
    "street, nature, urban, studio), time of day (day, night), "
    "activity (eating, working, talking, driving), mood (dramatic, comedic), "
    "and any prominent objects or visual elements. "
    "Return ONLY a raw JSON array of strings with no markdown, no code fences, no explanation. "
    'Example: ["person", "woman", "interior", "office", "day", "working"]'
)
# ─────────────────────────────────────────────────────────────────────────────


def get_api_key():
    if not os.path.exists(API_KEY_PATH):
        raise RuntimeError(
            f"API key not found. Save your Anthropic key as plain text at: {API_KEY_PATH}"
        )
    with open(API_KEY_PATH, "r") as f:
        return f.read().strip()


def get_poster_frames_dir():
    path = "/Volumes/<ProjectNickName>/<ProjectName>/02_Projects/09_Flame/_poster_frames"
    path = path.replace("<ProjectName>", str(flame.project.current_project.name))
    path = path.replace("<ProjectNickName>", str(flame.project.current_project.nickname))
    return path


def analyze_image(image_path, api_key):
    file_size = os.path.getsize(image_path)
    log(f"Sending image to Claude ({file_size} bytes): {image_path}")

    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": 256,
        "system": SYSTEM_PROMPT,
        "messages": [{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data,
                    },
                },
                {"type": "text", "text": "Tag this image."},
            ],
        }],
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=data,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw_response = response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"HTTP {e.code} from Anthropic API: {error_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error reaching Anthropic API: {e.reason}")

    log(f"Raw API response: {raw_response}")

    result = json.loads(raw_response)
    raw_tags = result["content"][0]["text"].strip()

    # Strip markdown code fences if present (```json ... ``` or ``` ... ```)
    raw_tags = re.sub(r"^```[a-z]*\n?", "", raw_tags)
    raw_tags = re.sub(r"\n?```$", "", raw_tags)
    raw_tags = raw_tags.strip()

    log(f"Raw tags from Claude: {raw_tags}")

    tags = json.loads(raw_tags)
    usage = result.get("usage", {})
    return [str(t).lower().strip() for t in tags if t], usage


def tag_clips(selection):
    try:
        _tag_clips(selection)
    except Exception:
        err = traceback.format_exc()
        log(f"UNHANDLED ERROR:\n{err}")


def _tag_clips(selection):
    global LOG_PATH

    log("Starting")

    try:
        api_key = get_api_key()
    except RuntimeError as e:
        log(f"ERROR: {e}")
        return

    clips = [c for c in selection if isinstance(c, flame.PyClip)]
    log(f"Clips found: {len(clips)}")
    if not clips:
        return

    poster_frames_dir = get_poster_frames_dir()
    log(f"Poster frames dir: {poster_frames_dir}")
    try:
        os.makedirs(poster_frames_dir, exist_ok=True)
    except Exception as e:
        log(f"ERROR creating folder: {e}")
        return

    exporter = flame.PyExporter()
    exporter.use_top_video_track = True
    exporter.foreground = True

    for clip in clips:
        clip_name = str(clip.name)[1:-1]
        clip_dir = os.path.join(poster_frames_dir, clip_name)

        try:
            os.makedirs(clip_dir, exist_ok=True)
        except Exception as e:
            log(f'ERROR creating clip folder "{clip_dir}": {e}')
            continue

        LOG_PATH = os.path.join(clip_dir, f"{clip_name}_log.txt")
        log(f'Processing: "{clip_name}"')

        try:
            exporter.export(clip, JPG_PRESET_PATH, clip_dir)
        except Exception as e:
            log(f'ERROR export failed for "{clip_name}": {e}')
            continue

        jpegs = sorted(
            glob.glob(os.path.join(clip_dir, "*.jpg")) +
            glob.glob(os.path.join(clip_dir, "*.jpeg"))
        )
        log(f"JPEGs found after export: {len(jpegs)}")
        if not jpegs:
            log(f'No frames exported for "{clip_name}" — skipping.')
            continue

        frame_path = jpegs[len(jpegs) // 2]
        log(f"Using frame: {os.path.basename(frame_path)}")

        try:
            tags, usage = analyze_image(frame_path, api_key)
        except Exception as e:
            log(f'ERROR analysis failed for "{clip_name}": {e}')
            continue

        input_tokens  = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)
        cost = (input_tokens * COST_PER_INPUT_TOKEN) + (output_tokens * COST_PER_OUTPUT_TOKEN)
        log(f"Tokens: {input_tokens} in / {output_tokens} out — cost: ${cost:.5f}")

        log(f"Applying tags: {tags}")
        clip.tags = tags
        clip.commit()
        log(f'"{clip_name}" → {", ".join(tags)}')

    log("Done.")


def scope_clip(selection):
    for item in selection:
        if isinstance(item, flame.PyClip):
            return True
    return False


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": FOLDER,
            "actions": [
                {
                    "name": "Tag Clips with AI",
                    "isVisible": scope_clip,
                    "execute": tag_clips,
                    "minimumVersion": "2024",
                }
            ],
        }
    ]
