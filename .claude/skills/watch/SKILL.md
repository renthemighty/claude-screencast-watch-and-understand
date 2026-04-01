---
name: watch
description: Process a screen recording and load its visual+audio context into the conversation. Triggered when the user types /watch or --watch followed by a file path (drag-and-drop from Finder works).
argument-hint: [path/to/recording.mov]
allowed-tools: Bash, Read
---

The user has provided a screen recording for you to analyse.

File path provided: $ARGUMENTS

## Steps

1. Run the video context script. Strip any trailing whitespace from the path. macOS drag-and-drop may add a trailing space:

```bash
python3 ~/bin/video_to_context.py $ARGUMENTS
```

If that fails due to special characters in the filename, copy it first:

```bash
cp $ARGUMENTS /tmp/watch_input.mov && python3 ~/bin/video_to_context.py /tmp/watch_input.mov
```

2. The context file is always saved to `~/Documents/GitHub/EasWrk/watched/` (or `$WATCH_DIR` if set). The filename is the video's stem + `.context.md` — e.g. `Screen Recording 2026-04-01.context.md`. Check that directory for the output file and read it.

3. Once read, respond with:
   - A 2-3 bullet summary of what was requested
   - Any key files, URLs, or identifiers mentioned
   - Ask the user to confirm before making any changes
