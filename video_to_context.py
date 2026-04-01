#!/usr/bin/env python3
"""
video_to_context.py — Feed a screen recording to Gemini and get a
timestamped visual+audio context document for Claude to read.

Usage:
    video_to_context.py recording.mov
    video_to_context.py recording.mp4 --output context.md

Output: saved to WATCH_DIR (default: ~/Documents/GitHub/EasWrk/watched/).
        Override with: export WATCH_DIR=/path/to/your/repo/watched
API key: set the GEMINI_API_KEY environment variable (required).

To upgrade from free tier to paid (same key, no script changes needed):
  https://aistudio.google.com/billing
Set a monthly spend cap at: https://aistudio.google.com/usage
"""

import sys
import os
import time
import argparse
import mimetypes
from pathlib import Path

TEST_KEY = ""

DEFAULT_WATCH_DIR = Path.home() / "Documents/GitHub/EasWrk/watched"

PROMPT = """You are helping a developer understand a screen recording so an AI coding assistant can act on it.

Watch this entire video carefully. Produce a structured context document with:

1. **Overview** (2-3 sentences): what is being shown and what the person wants done.

2. **Timestamped Log** — for every meaningful moment, one entry in this format:
   [MM:SS] SCREEN: <what is visible — app, file, UI element, text on screen, cursor position>
          AUDIO: <exactly or closely what was said, or "(no speech)">
          ACTION: <what the person did — clicked, scrolled, typed, highlighted, etc., or "(none)">

3. **Requested Changes** — a numbered list of every edit, change, or task the person asked for, extracted from both their words and what they pointed at on screen.

4. **Key Files / Paths** — any file names, URLs, function names, or identifiers visible or mentioned.

Be precise about UI elements — if they point at a button, name it. If they show code, quote the relevant line.
Do not summarize or skip sections — every spoken instruction matters."""


def get_api_key():
    return os.environ.get("GEMINI_API_KEY") or TEST_KEY


def upload_and_wait(client, video_path: Path, timeout_secs=300):
    mime, _ = mimetypes.guess_type(str(video_path))
    if not mime:
        mime = "video/mp4"

    print(f"Uploading {video_path.name} ({video_path.stat().st_size / 1024 / 1024:.1f} MB)...")

    with open(video_path, "rb") as f:
        file_ref = client.files.upload(
            file=f,
            config={"mime_type": mime, "display_name": video_path.name},
        )

    print(f"File URI: {file_ref.uri}")
    print("Waiting for Gemini to process video", end="", flush=True)

    deadline = time.time() + timeout_secs
    while time.time() < deadline:
        status = client.files.get(name=file_ref.name)
        state = str(status.state)
        if "ACTIVE" in state:
            print(" done.")
            return status
        elif "FAILED" in state:
            print()
            raise RuntimeError(f"Gemini file processing failed. State: {state}\nDetails: {status}")
        else:
            print(".", end="", flush=True)
            time.sleep(3)

    print()
    raise TimeoutError(f"Timed out after {timeout_secs}s waiting for file to become ACTIVE. Last state: {state}")


def generate_context(api_key: str, video_path: Path) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    file_ref = upload_and_wait(client, video_path)

    print("Analysing video...")
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            types.Part.from_uri(file_uri=file_ref.uri, mime_type=file_ref.mime_type),
            PROMPT,
        ],
    )

    # Clean up uploaded file
    try:
        client.files.delete(name=file_ref.name)
    except Exception:
        pass

    return response.text


def main():
    parser = argparse.ArgumentParser(description="Convert a screen recording to a Claude context document.")
    parser.add_argument("video", help="Path to the video file (.mov, .mp4, .mkv, etc.)")
    parser.add_argument("--output", "-o", help="Output .md path (default: <video>.context.md)")
    args = parser.parse_args()

    video_path = Path(args.video).expanduser().resolve()
    if not video_path.exists():
        print(f"Error: file not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
    else:
        watch_dir = Path(os.environ.get("WATCH_DIR", DEFAULT_WATCH_DIR)).expanduser().resolve()
        watch_dir.mkdir(parents=True, exist_ok=True)
        output_path = watch_dir / (video_path.stem + ".context.md")

    api_key = get_api_key()
    if not api_key:
        print("Error: set GEMINI_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    try:
        context = generate_context(api_key, video_path)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)

    output_path.write_text(context, encoding="utf-8")
    print(f"\nContext written to: {output_path}")
    print(f"Feed to Claude: read {output_path}")


if __name__ == "__main__":
    main()
