# AGENT_GUIDE.md — StickLit AI Agent Operating Manual (v2.1)

> **Who this is for**: AI agents, automated workers, and developers who need to produce a  
> complete StickLit video from scratch — or render one from existing assets.  
>  
> **Read this file top-to-bottom before touching any command.**

---

## SECTION 0: Understand the Repo in 30 Seconds

```
INPUT  →  script.txt + images folder
PROCESS →  sticklit.py (audit → render)
OUTPUT  →  output/<book>/MASTER_FINAL.mp4
```

The only command you need is `sticklit.py`. Everything else is pre-built.

---

## SECTION 1: Non-Negotiable Production Rules

Violating any of these = reject and restart.

### Rule 1 — Runtime: 2:00 to 3:00 minutes (HARD LIMITS)
- Audio voiceover must be **130s – 170s**
- Script must be **340 – 460 words** (at ~150 WPM)
- Scripts under 2 minutes are **forbidden** — they feel compressed and rushed

### Rule 2 — Organic Scene Cuts (NEVER a fixed number)
- Cuts happen on narrative shifts and punchlines — **not on a timer**
- Typical result: ~45–55 scenes for a 2:30 video
- Average scene duration: **2.8s – 3.3s**
- **Never lock to 38 or any arbitrary number**

### Rule 3 — Locked Canonical Characters
**Kai (Boy)**:
- Circular head, flat warm natural skin tone (NOT white, NOT pink — warm tan)
- Messy spiky jet-black hair
- Dark charcoal short-sleeve tee `#3A3A3C`
- Grey stick trousers `#8E8E93`
- Black boots
- Confident knowing smirk, 2D stick limbs (zero muscular bulk)

**Maya (Girl)**:
- Circular head, same flat warm natural skin tone
- High spiky black ponytail with fringe bangs
- Same charcoal tee `#3A3A3C`, grey trousers `#8E8E93`, black boots
- Analytical wink, 2D stick limbs (zero muscular bulk)

**Negative directives for every prompt** (add to ALL prompts):  
`(defined muscles, thick muscular limbs, realistic human anatomy, 3D render, dark background, borders, gradients, shadows)`

### Rule 4 — Scene 01: The Book Cover (ZERO TILT LAW)
- Book must be **centered, 100% upright, flat-facing the camera, perfectly level**
- Title lettering must be **100% horizontal** — viewer must read it with zero head tilt
- Flanked by Kai (left) and Maya (right) in money/power/relevant stances
- **Zero tilt. Zero rotation. Zero neck bending. No exceptions.**

### Rule 5 — Last Scene: The VS Split Screen (ONE IMAGE)
- A single cohesive 9:16 image split horizontally down the middle
- Top panel = negative choice (trapped, stressed, chained)
- Bottom panel = positive choice (free, peaceful, sovereign)  
- Central circular `(VS)` badge on the dividing line
- **Generated as ONE single image — never two stitched images**

### Rule 6 — Golden Subtitles (IMMOVABLE)
- Font: Arial Black, Size 58
- Color: **Golden Yellow `#FFE600`** (ASS BGR hex: `&H0000E6FF`)
- Border: **5.0px solid black**
- `MarginV = 100`
- Bottom 250px of every frame = pure white `#FFFFFF` — subtitle safe zone, no artwork

---

## SECTION 2: Full Production Workflow

### PHASE A — Script (Do This If Starting from Scratch)

**Step A1: Research the Book**
- Read the book's core thesis, paradoxes, and key stories
- Identify the central contrarian hook (what most people get wrong)
- Find 2–3 concrete unforgettable stories/examples from the book
- Identify the final binary dilemma (the ending "VS" question)

**Step A2: Write the Script**

Use this 4-Act Structure:

```
Act 1 — Contrarian Hook (0:00 – 0:15s, ~35 words)
  - Open with the belief everyone holds that is completely wrong
  - Drop a shocking statistic or contrasting character comparison

Act 2 — The Trap (0:15 – 0:45s, ~75 words)
  - Show the concrete story that proves the paradox
  - Use real names, real numbers, real contrast

Act 3 — The Laws (0:45 – 2:00, ~180 words)
  - Present 3–4 non-obvious rules/laws from the book
  - Each law starts with a single word: "First,", "Second,", "Third,"
  - Each law should have a physical visual metaphor embedded in the language

Act 4 — The Dilemma (2:00 – 2:30, ~70 words)
  - Deliver the life-changing epiphany
  - End with the binary VS question for the audience to comment on
```

**Word count target**: 380–430 words  
**Test**: Paste into any text-to-speech tool. Should read at ~150 WPM = 2:30 min.

---

### PHASE B — Audio (Voiceover + Alignment)

**Step B1: Synthesize Voiceover**
```bash
python sticklit.py synthesize --book <book_slug>
```
Uses Deepgram Aura-2 (`aura-2-thalia-en`). Outputs `output/<book>/<book>_voiceover.mp3`.

**Step B2: Verify Duration**
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 output/<book>/<book>_voiceover.mp3
```
- ✅ Accept: 130s – 170s
- ❌ Reject: < 120s → expand the script by 50+ words and re-synthesize
- ❌ Reject: > 180s → trim 1–2 stories and re-synthesize

**Step B3: Align Words (Get Timestamps)**
```bash
python sticklit.py align --book <book_slug>
```
Sends audio to Deepgram Nova-2. Outputs `books/<book>/timestamps.json` (word-level millisecond timestamps).

**Step B4: Generate Scene Cut Boundaries**
```bash
python sticklit.py cues --book <book_slug>
```
Reads `timestamps.json` + `script.txt`, finds thought-shift boundaries, outputs `books/<book>/exact_cues.json`.

**Step B5: Generate Golden Subtitles**
```bash
python sticklit.py subtitles --book <book_slug>
```
Reads timestamps, outputs `books/<book>/golden_subtitles.ass` (Golden Yellow `#FFE600`, 5.0px, MarginV=100).

---

### PHASE C — Image Prompts

**Step C1: Write the Prompts**

Open `books/<book>/exact_cues.json`. There will be N scenes.  
Write one prompt per scene. Save to `books/<book>/prompts.txt`.

**EVERY prompt must start with this prefix:**
```
[SCENE_XX] 9:16 vertical 2D minimalist cartoon stick-figure illustration in the exact @sticklit style.
Pure borderless white background (#FFFFFF) with abundant clean negative space.
Crisp solid black ink outlines, flat solid color fills, zero 3D rendering, zero gradients,
zero background clutter. Near the top center, small subtle text: '@sticklit'.
Bottom 250px is completely clear white negative space.
```

**Scene 01 prompt must include:**
- Centered colossal upright book facing the camera flat (zero tilt)
- Bold horizontal gold lettering: "[BOOK TITLE]" / "[AUTHOR]" / "in two minutes"
- Kai left, Maya right, in relevant power stances

**Last scene prompt must include:**
- Single 9:16 horizontal split-screen image (NOT two separate images)
- Top panel vs Bottom panel with central `(VS)` badge
- Specific contrasting scenarios tied to the book's ending dilemma

**For all middle scenes:**
- Each scene should reflect the exact words spoken during that scene's timestamp window
- Use physical, visual metaphors — avoid abstract text descriptions
- Kai and Maya appear in scenes where the story involves human action
- Props appear in isolation for conceptual scenes (treadmill, anvil, snowball, ladder, etc.)

**Step C2: Build the Signature Manifest (for fast image matching)**
```bash
python sticklit.py manifest --book <book_slug>
```
Reads `prompts.txt`, extracts a unique visual signature for each scene, outputs `books/<book>/prompts_manifest.json`.  
This allows `sticklit.py` to instantly map any AI-generated image filename to its correct scene in 0.1 seconds.

---

### PHASE D — Images (External Step — You Do This)

1. Take the prompts from `books/<book>/prompts.txt`
2. Send them to your image generator of choice (Midjourney, DALL·E, Gemini, etc.)
3. Download all images into **a single flat folder** (do not organize into subfolders)

**Naming — Two Options:**
- **Option A (Best)**: Name them `scene_01.jpg`, `scene_02.jpg`, … `scene_50.jpg` — instant match
- **Option B (Any name)**: The engine will auto-match using visual signature keywords in the filename

---

### PHASE E — Render

**Step E1: Audit (mandatory before render)**
```bash
python sticklit.py audit --book <book_slug> --images "C:\path\to\images"
```

Expected terminal output:
```
[SUCCESS] 50/50 scenes matched perfectly. Zero collisions. Ready to render.
```

If any scenes show `[UNMATCHED]`, rename those image files to `scene_XX.jpg` format for that scene number.

**Step E2: Render the Master Video**
```bash
python sticklit.py render --book <book_slug> --images "C:\path\to\images"
```

What this does (in order):
1. Normalizes every image to 1080×1920 pure white (Lanczos scaling, letterbox fill)
2. Builds a CFR 30fps hardlink frame sequence (~4,640 frames for a 154s video)
3. Encodes raw video with FFmpeg libx264 (yuv420p, CRF 18)
4. Burns `golden_subtitles.ass` at MarginV=100 with the 250px safety zone
5. Mixes ducked BGM at -18.4 dB under voiceover
6. Outputs: `output/<book_slug>/<book_slug>_MASTER_FINAL.mp4`

**Step E3: Verify the output**
```bash
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 output/<book>/<book>_MASTER_FINAL.mp4
```
- ✅ Duration: 130 – 170 seconds
- ✅ Frame rate: `30.000 fps` (not 29.97, not VFR)
- ✅ File size: 8 MB – 20 MB typical

---

## SECTION 3: Command Reference

```bash
# Full pipeline from scratch:
python sticklit.py synthesize  --book <slug>
python sticklit.py align       --book <slug>
python sticklit.py cues        --book <slug>
python sticklit.py subtitles   --book <slug>
python sticklit.py manifest    --book <slug>

# Image matching + render:
python sticklit.py audit       --book <slug>  --images "<path>"
python sticklit.py render      --book <slug>  --images "<path>"
```

### `--book` argument
Pass the folder name inside `books/`. Examples:
- `psychology_of_money`
- `48_laws_of_power`
- `atomic_habits`
- `deep_work` (not yet produced — create the folder first)

### `--images` argument
Path to the folder containing your downloaded AI-generated images.  
The engine accepts `.jpg`, `.jpeg`, `.png`, `.webp` — mixed in the same folder is fine.

---

## SECTION 4: File Reference — What Goes Where

```
books/<book_slug>/
│
├── script.txt              INPUT   Your 380–430 word narration script
├── timestamps.json         GENERATED  Deepgram Nova-2 word timestamps (auto)
├── exact_cues.json         GENERATED  Scene cut boundaries (auto)
├── golden_subtitles.ass    GENERATED  Pre-built golden subtitles (auto)
├── prompts.txt             INPUT   50 tagged image prompts [SCENE_XX]
└── prompts_manifest.json   GENERATED  Regex signature map for image matching (auto)

output/<book_slug>/
├── <book>_voiceover.mp3    GENERATED  TTS audio (gitignored)
└── <book>_MASTER_FINAL.mp4 GENERATED  Final video (gitignored)
```

**What you provide**: `script.txt` + `prompts.txt` + image folder  
**What the pipeline generates**: everything else

---

## SECTION 5: Troubleshooting Rules

| Problem | Fix |
| :--- | :--- |
| Audio duration < 120s | Script too short. Expand by 50+ words. Re-synthesize. |
| Unmatched scenes in audit | Rename those files to `scene_XX.jpg` for the scene number |
| Subtitle drift | Always use CFR (`-vsync cfr`). Never VFR. |
| Subtitle cut off at bottom | Check `MarginV = 100` in .ass file. Bottom 250px must be clear. |
| Book art misaligned | Scene 01 image must have zero tilt. Regenerate if needed. |
| PowerShell complex string errors | Write a `.py` script — never inline complex JSON in PS |
| Last scene looks stitched | Must be ONE image. Regenerate with "single cohesive split-screen" in prompt. |
| Video file too large (>25 MB) | Check CRF — should be 18. Raise to 22 if needed. |

---

## SECTION 6: Master Benchmark Reference

| Book | Scenes | Duration | File Size | Drift |
| :--- | :--- | :--- | :--- | :--- |
| **The Psychology of Money** ✅ | 50 | **154.66s (2:34)** | 12.45 MB | 0.000% |
| The 48 Laws of Power | 38 | ~155s | — | — |
| Atomic Habits | 38 | ~150s | — | — |

**The Psychology of Money** in `books/psychology_of_money/` is the gold-standard reference.  
When in doubt, compare your output to this benchmark.
