# books/ — Book Asset Catalog

Each subfolder is one self-contained book production.

## How to Add a New Book

1. Create a new folder: `books/<book_slug>/`  
   Use lowercase with underscores: `deep_work`, `thinking_fast_and_slow`, `the_richest_man_in_babylon`

2. Add these two files (everything else is auto-generated):
   - `script.txt` — your 380–430 word narration script
   - `prompts.txt` — your image prompts tagged `[SCENE_01]` through `[SCENE_N]`

3. Run the pipeline:
   ```bash
   python sticklit.py align     --book <slug>
   python sticklit.py cues      --book <slug>
   python sticklit.py subtitles --book <slug>
   python sticklit.py manifest  --book <slug>
   python sticklit.py audit     --book <slug> --images "<path>"
   python sticklit.py render    --book <slug> --images "<path>"
   ```

## Books Status

| Book | Slug | Scenes | Status |
| :--- | :--- | :--- | :--- |
| The Psychology of Money | `psychology_of_money` | 50 | ✅ Master Benchmark (154s, 50 Scenes) |
| Atomic Habits | `atomic_habits` | 44 | ✅ Full Catalog Ready (134s, 44 Cues, Prompts) |
| The 48 Laws of Power | `48_laws_of_power` | 38 | ✅ Produced |

## Required File Format: `script.txt`

Plain text. No markdown. No asterisks. No scene labels.  
Just the exact words the voiceover speaks, in paragraphs.

```
The psychology of money by Morgan Housel in two minutes.

Most people believe getting rich is about finance formulas...
```

## Required File Format: `prompts.txt`

One prompt block per scene. Each block starts with the `[SCENE_XX]` tag.  
Blank line between scenes.

```
[SCENE_01] 9:16 vertical cover illustration...
<full prompt text>

[SCENE_02] 9:16 vertical scene...
<full prompt text>
```

## Do NOT commit to this folder
- Audio files (`.mp3`, `.wav`)
- Video files (`.mp4`)
- Image files (`.jpg`, `.png`) — images live in a local folder you point `sticklit.py` to
