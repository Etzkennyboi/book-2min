# 📚 StickLit — Viral 2D Stickman Book Summary Video Pipeline

> **Clone → Add your API key → Give it a book name + your images → Get a ready-to-upload video.**

StickLit is a fully autonomous production pipeline that converts any book into a **2–3 minute viral 9:16 vertical animated webcomic video** in the signature `@sticklit` style — hard-cut scenes, golden subtitles, locked canonical characters, and zero drift.

---

## 🗂️ Repository Map

```text
sticklit/
│
├── README.md                      ← You are here. Start here.
├── AGENT_GUIDE.md                 ← Step-by-step instructions for AI agents
├── sticklit.py                    ← THE single command to audit or render any book
├── requirements.txt               ← Python dependencies
├── .env.example                   ← Copy to .env and fill in your Deepgram API key
│
├── pipeline/                      ← All reusable pipeline modules
│   ├── config.py                  ← Constants: canvas size, FPS, subtitle colors
│   ├── tts_engine.py              ← Deepgram Aura-2 TTS (+ Edge-TTS fallback)
│   ├── speech_aligner.py          ← Deepgram Nova-2 word-level timestamp aligner
│   ├── subtitle_generator.py      ← Golden ASS subtitle builder (#FFE600)
│   ├── audio_mixer.py             ← BGM ducking mixer (-18.4 dB under VO)
│   └── video_renderer.py          ← CFR 30fps frame assembler + FFmpeg encoder
│
├── books/                         ← One folder per book. Each folder is self-contained.
│   └── psychology_of_money/       ← ✅ MASTER BENCHMARK (50 scenes, 154.66s, 0.000% drift)
│       ├── script.txt             ← 386-word narration script
│       ├── prompts.txt            ← 50 image prompts tagged [SCENE_01]…[SCENE_50]
│       ├── prompts_manifest.json  ← Regex signature map: scene number → file slug
│       ├── exact_cues.json        ← 50 organic cut timestamps (from Deepgram alignment)
│       ├── golden_subtitles.ass   ← Pre-built ASS subtitles (#FFE600, 5.0px border)
│       └── timestamps.json        ← Raw Deepgram Nova-2 word timestamps
│
└── examples/                      ← Reference assets for already-produced books
    └── rich_dad_poor_dad/
        ├── script.txt
        ├── prompts.json
        └── metadata.json
```

> **`output/` and image folders are gitignored** — they are produced locally and never committed.

---

## ⚡ Quickstart (5 Steps)

### 1. Clone & Install
```bash
git clone https://github.com/Etzkennyboi/book-2min.git
cd book-2min
pip install -r requirements.txt
```

### 2. Set your API Key
```bash
cp .env.example .env
# Open .env and paste your Deepgram API key
```
> Get a free key at [console.deepgram.com](https://console.deepgram.com)

### 3. Generate your images externally
Use any AI image generator (Midjourney, DALL·E, Gemini, etc.) with the prompts from `books/<book>/prompts.txt`.  
Name your files `scene_01.jpg`, `scene_02.jpg`, … OR name them anything — the engine will auto-match.

### 4. Audit (verify 100% matching before rendering)
```bash
python sticklit.py audit --book psychology_of_money --images "C:\path\to\your\images"
```

### 5. Render the final video
```bash
python sticklit.py render --book psychology_of_money --images "C:\path\to\your\images"
```
Output: `output/psychology_of_money/psychology_of_money_MASTER_FINAL.mp4`

---

## 🎬 What the Output Looks Like

| Property | Value |
| :--- | :--- |
| Resolution | 1080 × 1920 (9:16 vertical) |
| Frame Rate | CFR 30.000 fps (zero drift) |
| Runtime | 130s – 170s (2:00 – 3:00 min) |
| Scenes | ~45–55 organic hard cuts |
| Subtitles | Golden Yellow `#FFE600`, Arial Black 58pt, 5px black border |
| Audio | Deepgram Aura-2 VO + ducked BGM |
| Benchmark | *Psychology of Money* → 154.66s, 50 scenes, 12.45 MB |

---

## 📖 Adding a New Book

See **[AGENT_GUIDE.md](AGENT_GUIDE.md)** for the full step-by-step.

Short version:
1. Create `books/<book_slug>/` folder
2. Write `script.txt` (340–460 words)
3. Run TTS + alignment to generate `exact_cues.json`
4. Write 50 tagged prompts → `prompts.txt`
5. Generate images externally → run `sticklit.py render`

---

## 🔑 Environment Variables

| Variable | Required | Description |
| :--- | :--- | :--- |
| `DEEPGRAM_API_KEY` | ✅ Yes | Deepgram API key for TTS and word alignment |
| `DEEPGRAM_VOICE_MODEL` | Optional | Defaults to `aura-2-thalia-en` |
| `EDGE_TTS_VOICE` | Optional | Free fallback TTS if no Deepgram key |

---

## 🧠 Character Bible (Never Change These)

| Character | Description |
| :--- | :--- |
| **Kai** (Boy) | Messy spiky black hair · flat warm skin · charcoal tee `#3A3A3C` · grey pants `#8E8E93` · black boots · confident smirk |
| **Maya** (Girl) | High spiky black ponytail + bangs · flat warm skin · same outfit as Kai · analytical wink |
| **Canvas** | Pure white `#FFFFFF` · 1080×1920 · bottom 250px subtitle-safe zone always clear |
| **Scene 01 rule** | Book is ALWAYS centered, 100% upright, zero tilt — flanked by Kai & Maya |
| **Last scene rule** | Always a single horizontal split-screen VS image (one image, not stitched) |
