# Claude ScreenCast Watch and Understand

Screen record yourself explaining what you want changed. This tool watches the video, transcribes what you said, reads what was on screen, and hands Claude Code a structured brief so it can act on it without any further explanation.

## How it works

1. You screen record with narration
2. Run `/watch` (or drag the file into the terminal after `--watch`)
3. The video goes to Gemini, which produces a timestamped log of everything visible and everything said
4. That context file lands in your `watched/` folder
5. Claude Code reads it and gets to work

## Requirements

- Python 3.9+
- `pip install google-genai`
- A Gemini API key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

## Setup

### 1. Install the script

```bash
cp video_to_context.py ~/bin/video_to_context.py
chmod +x ~/bin/video_to_context.py
```

Make sure `~/bin` is in your PATH. Add to `~/.zshrc` if not:

```bash
export PATH="$HOME/bin:$PATH"
```

### 2. Set your API key

```bash
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.zshrc
```

To upgrade from free tier to paid (same key, no changes needed):
- Upgrade: https://aistudio.google.com/billing
- Set a spend cap: https://aistudio.google.com/usage

### 3. Set your watched folder

By default, context files are saved to `~/Documents/GitHub/EasWrk/watched/`. Override with:

```bash
echo 'export WATCH_DIR="/path/to/your/repo/watched"' >> ~/.zshrc
```

### 4. Install the Claude Code skill

Copy the skill into your personal Claude skills folder:

```bash
mkdir -p ~/.claude/skills/watch
cp .claude/skills/watch/SKILL.md ~/.claude/skills/watch/
```

## Usage

### From the terminal

```bash
video_to_context.py ~/Desktop/recording.mov
```

### From Claude Code

Type `/watch` then drag and drop your screen recording into the terminal:

```
/watch /path/to/recording.mov
```

Claude will process the video, read the context file, summarise what was requested, and ask you to confirm before making any changes.

## Output

Each recording produces a `.context.md` file in your `watched/` folder containing:

- **Overview** — what was shown and what was asked for
- **Timestamped log** — screen state, spoken audio, and cursor actions at each moment
- **Requested changes** — numbered list of every task extracted from the video
- **Key files and paths** — any file names, URLs, or identifiers mentioned or visible

## Notes

- macOS screen recordings contain a Unicode narrow no-break space before "AM/PM" in the filename. The skill handles this automatically by copying to a temp path before processing.
- Uploaded files are deleted from Gemini immediately after processing.
- Context files are plain markdown — you can read, edit, or reference them any time.
