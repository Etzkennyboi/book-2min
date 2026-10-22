# StickLit AI Agent Production Playbook (v2.1)

> **Audience**: AI Coding Agents, Automated Production Workers, and Developers  
> **Repository Purpose**: Autonomous pipeline for generating viral, high-retention 9:16 vertical animated webcomic book summaries (2:00 – 3:00 min).  
> **Current Master Benchmark**: *The Psychology of Money* by Morgan Housel (154.66s / 50 organic scenes / CFR 30fps).  

---

## 1. Non-Negotiable Master Standards

Every production run **MUST** strictly adhere to these 6 golden rules:

1. **Strict 2:00 – 3:00 Minute Runtime**:
   - Total audio and video runtime must land between **130.0s and 170.0s** (~340–460 spoken words).
   - Scripts shorter than 2:00 (e.g. 107s) are **strictly forbidden** (too compressed).
2. **Organic Script-Driven Cuts (No Rigid Quota)**:
   - Cuts must occur organically on narrative shifts and punchlines (typically ~45–55 cuts for a 2.5-minute video; average cut length: 2.8s–3.3s).
   - **Never lock to an arbitrary figure like 38**.
3. **Canonical Protagonist Duo (Kai & Maya)**:
   - **Boy ("Kai")**: Messy spiky black hair, arched comic brow, confident smirk, circular head with flat warm natural skin tone, minimalist 2D stick limbs (zero muscular bulk), dark charcoal tee (`#3A3A3C`), grey stick trousers (`#8E8E93`), black boots.
   - **Girl ("Maya")**: High spiky black ponytail with fringe bangs, analytical wink, circular head with flat warm natural skin tone, minimalist 2D stick limbs, charcoal tee (`#3A3A3C`), grey stick trousers (`#8E8E93`), black boots.
   - **Negative Directives**: `(defined muscles, thick muscular limbs, realistic human anatomy, 3D render, dark background, borders)`.
4. **Scene 01: Centered Colossal Upright Book (Zero Tilt Rule)**:
   - The book stands **centered, 100% upright, flat-facing, and level** to the camera.
   - Title and author in **bold, perfectly horizontal gold lettering**.
   - **Zero tilt / zero rotation / zero neck bending**! Flanked by Kai and Maya in power stances.
5. **Scene Last: Single Cohesive Horizontal Split Screen**:
   - Top-vs-bottom horizontal split divided by a black line with a central circular **`(VS)`** badge.
   - Generated as **one single 9:16 image**, never stitched from separate files.
6. **Golden Subtitle Standard**:
   - Style: Arial Black, Size 58, **Golden Yellow (`#FFE600`, ASS BGR `&H0000E6FF`)**, **5.0px black border**, `MarginV = 100`.
   - Subtitle Safety Zone: All visual artwork placed in the upper 80%; bottom 250px must remain pure white negative space.

---

## 2. Directory Architecture

```text
eager-planck/
├── sticklit.py                  # Master Turnkey CLI Entrypoint (audit & render)
├── AI_AGENT_WORKFLOW.md         # This autonomous operating manual
├── README.md                    # Repository documentation
├── books/                       # Golden assets for verified books
│   ├── psychology_of_money/     # Current 50-Scene Benchmark
│   │   ├── script.txt           # Verified 386-word narrative script
│   │   ├── exact_cues.json      # 50 organic cut boundaries with exact timestamps
│   │   ├── golden_subtitles.ass # #FFE600 5.0px border ASS subtitles
│   │   ├── prompts_50_scenes.txt# 50 prompts with [SCENE_XX] tags
│   │   ├── prompts_manifest.json# 1-to-1 slug & signature regex map
│   │   └── timestamps.json      # Deepgram Nova-2 word timestamps
│   ├── 48_laws_of_power/        # Verified 38-Scene Release
│   └── atomic_habits/           # Verified 38-Scene Release
├── src/                         # Modular pipeline libraries
│   ├── config.py                # Global constants (1080x1920, 30fps, API keys)
│   ├── tts_engine.py            # Deepgram Aura-2 / Edge-TTS synthesizer
│   ├── speech_aligner.py        # Nova-2 word-level aligner
│   ├── subtitle_generator.py    # ASS karaoke and phrased generator
│   ├── audio_mixer.py           # Ducked BGM mixer (-18.4 dB)
│   └── video_renderer.py        # CFR video encoder
└── output/                      # Rendered releases & temporary working caches
    └── psychology_of_money/
        ├── psychology_of_money_MASTER_FINAL.mp4 # Verified 12.45 MB master video
        └── psychology_of_money_voiceover.mp3    # 154.66s studio narration
```

---

## 3. Fast Agent Command Playbook

### Step 1: Pre-Render Ingestion Audit
When a user provides a directory containing generated images, verify 100% matching:
```bash
python sticklit.py audit --book psychology_of_money --images "C:\path\to\downloaded_images"
```
*Expected Output*: Displays the 50-row audit manifest and terminates with `[SUCCESS] 100% of all 50 scenes matched perfectly!`.

### Step 2: Render Master 9:16 Video
To normalize frames to 1080x1920 pure white, build the 30.000 fps CFR sequence, burn golden subtitles, and mix ducked BGM:
```bash
python sticklit.py render --book psychology_of_money --images "C:\path\to\downloaded_images"
```
*Output File*: `output/psychology_of_money/psychology_of_money_MASTER_FINAL.mp4`

### Step 3: Produce a New Book from Scratch
To produce an entirely new book:
1. **Research & Script**: Write a 340–460 word script following the 4-Act Engine (Contrarian Hook, Naive Trap, 3 Non-Obvious Laws, Final Binary Dilemma).
2. **Synthesize Voiceover**: Use Deepgram Aura-2 Thalia (`aura-2-thalia-en`) and align with Nova-2.
3. **Partition Cuts**: Generate `exact_cues.json` based on thought shifts (avg 2.8s–3.2s per scene).
4. **Draft Prompts**: Write tagged prompts starting with `[SCENE_01]`, `[SCENE_02]`... ensuring Scene 01 is an upright centered book and Scene Last is a single horizontal split screen.
5. **Execute Render**: Run `python sticklit.py render --book <slug> --images <folder>`.

---

## 4. Key Troubleshooting Rules for Agents

1. **Never use PowerShell inline quotes for complex JSON/Python strings**: Always write a `.py` script or invoke `sticklit.py`.
2. **Always verify audio duration first**: Run `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <audio.mp3>`. If `< 120s`, reject and expand the script.
3. **Always use Constant Frame Rate (CFR 30.00 fps)**: Never use variable frame rate (`-vsync vfr`) because ASS subtitles will drift out of synchronization.
4. **Subtitle Safety Clearance**: The bottom 250px of every single frame must remain clear pure white `#FFFFFF` negative space.
