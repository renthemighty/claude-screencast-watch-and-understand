# 🎬 Claude ScreenCast Watch and Understand

> Record your screen. Talk through what you want. Let Claude act on it.

Instead of typing out long instructions, screen record yourself pointing at things and explaining what needs to change. This tool watches the video, reads what was on screen, transcribes what you said, and hands Claude Code a structured brief — timestamps, requested changes, key file paths, all of it — so it can get straight to work.

---

## How it works

```
You record  →  Gemini watches  →  Context file saved  →  Claude reads and acts
```

1. Screen record with narration (QuickTime, OBS, anything)
2. Type `/watch` in Claude Code and drag the file in
3. Gemini processes the full video — visuals and audio together
4. A `.context.md` file lands in your `watched/` folder
5. Claude reads it, summarises what you asked for, and gets to work

---

## Why Gemini for this?

Gemini watches the video as a single unified stream — cursor position, screen content, and your voice all understood together in the same moment. The alternative (frame extraction + separate transcription) produces two misaligned data streams you'd have to mentally stitch. This produces one coherent brief.

---

## Requirements

- Python 3.9+
- `pip install google-genai`
- A Gemini API key → [aistudio.google.com/apikey](https://aistudio.google.com/apikey) (free tier works)
- Claude Code

---

## Setup

### 1. Install the script

```bash
cp video_to_context.py ~/bin/video_to_context.py
chmod +x ~/bin/video_to_context.py
```

Add `~/bin` to your PATH if it isn't already (`~/.zshrc` or `~/.bashrc`):

```bash
export PATH="$HOME/bin:$PATH"
```

### 2. Add your API key

```bash
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.zshrc
```

**Free tier is enough to start.** When you need to upgrade, same key — just connect billing at [aistudio.google.com/billing](https://aistudio.google.com/billing). Set a monthly spend cap at [aistudio.google.com/usage](https://aistudio.google.com/usage).

### 3. Set your watched folder

Context files save to `~/Documents/GitHub/EasWrk/watched/` by default. Override with:

```bash
echo 'export WATCH_DIR="/path/to/your/repo/watched"' >> ~/.zshrc
```

### 4. Install the Claude Code skill

```bash
mkdir -p ~/.claude/skills/watch
cp .claude/skills/watch/SKILL.md ~/.claude/skills/watch/
```

---

## Usage

### From Claude Code (recommended)

Type `/watch` and drag your recording straight into the terminal:

```
/watch /Users/you/Desktop/recording.mov
```

Claude processes the video, reads the context file, gives you a bullet summary of every requested change, and asks you to confirm before touching anything.

### From the terminal directly

```bash
video_to_context.py ~/Desktop/recording.mov
```

Output goes to `$WATCH_DIR/recording.context.md`.

---

## What the context file looks like

```markdown
### Overview
The developer is comparing the live shop page with a local concept file.
They want the header updated to be full-width and positioned above the content block.

### Timestamped Log
| Timestamp | Screen | Audio | Action |
|---|---|---|---|
| 00:00 | jeff.pioneerpuff.co/shop — logo and nav in narrow container | "the header is supposed to be full screen..." | Circled the nav area |
| 00:16 | Local concept-shop.html — full-width header visible | "...as it is in the concept" | Switched tabs |

### Requested Changes
1. Full-width header on the live shop page
2. Header positioned above the content block, matching concept-shop.html

### Key Files / Paths
- Live: https://jeff.pioneerpuff.co/shop
- Reference: /Users/you/Documents/concept-shop.html
```

---

## Notes

- macOS screen recordings have a Unicode narrow no-break space before AM/PM in the filename. The skill handles this automatically.
- Files are deleted from Gemini immediately after processing — nothing is retained remotely.
- Context files are plain markdown. Read, edit, or reference them any time.
- The `watched/` folder is git-tracked but `.context.md` files are gitignored by default.

---

## File structure

```
.
├── video_to_context.py          # Main script — uploads video, calls Gemini, writes context
├── .claude/
│   └── skills/
│       └── watch/
│           └── SKILL.md         # Claude Code /watch skill definition
└── watched/                     # Context files land here (gitignored)
```
