# books/psychology_of_money — Master Benchmark Book

This folder is the **gold-standard reference** for the StickLit pipeline.  
Every future book must produce assets in exactly this same format.

## Files in This Folder

| File | Type | Description |
| :--- | :--- | :--- |
| `script.txt` | **You provide** | 386-word narration script (verbatim what the voiceover says) |
| `prompts.txt` | **You provide** | 50 image prompts, each tagged `[SCENE_01]` through `[SCENE_50]` |
| `timestamps.json` | Auto-generated | Deepgram Nova-2 word-level timestamps (run `sticklit.py align`) |
| `exact_cues.json` | Auto-generated | 50 organic scene cut boundaries with start/end seconds |
| `golden_subtitles.ass` | Auto-generated | Pre-built ASS subtitle file (Golden Yellow `#FFE600`, 5.0px border) |
| `prompts_manifest.json` | Auto-generated | Visual keyword signatures for 0.1s image-to-scene matching |

## Stats
- **Scenes**: 50
- **Runtime**: 154.66s (2:34)
- **Words**: 386
- **CFR**: 30.000 fps
- **Timing drift**: 0.000%

## How Prompts Are Tagged

Every prompt in `prompts.txt` starts with `[SCENE_XX]`:
```
[SCENE_01] 9:16 vertical cover illustration for 'The Psychology of Money'...
[SCENE_02] 9:16 vertical scene. Kai holds a massive janitor mop...
...
[SCENE_50] Single cohesive 9:16 horizontal split-screen VS image...
```

This tag is how `sticklit.py audit` and `sticklit.py render` know which image belongs to which scene.

## How Image Matching Works

When you give images to `sticklit.py`, it matches them to scenes in this priority order:
1. **Regex tag match**: if filename contains `scene_01`, `scene_02`, etc. → instant match
2. **Signature keyword match**: checks filename against the unique visual keywords in `prompts_manifest.json`

Name your image files `scene_01.jpg` through `scene_50.jpg` for the fastest, most reliable matching.
