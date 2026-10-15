# 📚 Book-2Min

> **High-Retention StickLit Animated Book Summary Video Generator**  
> Automated end-to-end pipeline for turning any non-fiction book into a viral 2-minute, 9:16 vertical animated video in the visual style of `@sticklit`.

---

## 🎯 Overview

Book summaries on TikTok, YouTube Shorts, and Instagram Reels live or die by **audience retention**. Standard talking-head videos or slow slideshows suffer from steep viewer drop-offs.

**Book-2Min** replicates the viral animated format popularized by channels like `@sticklit` (commanding 10M+ views), engineered specifically for maximum watch time:
- **Fast-Paced Visual Cuts**: 40 unique scene illustrations for a 147-second video (~3.68s per image), preventing visual fatigue.
- **The Everyman Visual Identity**: A consistent, instantly recognizable protagonist—a black-ink stick figure wearing a crisp white collared shirt and thin black necktie.
- **Pure Full-Frame 9:16 Art**: No artificial zooming or panning across horizontal crops. Every illustration is composed natively for vertical mobile screens with distressed headlines and callout tags.
- **Deepgram Flagship Voiceover**: Powered by Deepgram Aura-2 Thalia (`aura-2-thalia-en`), delivering natural, engaging, and professional narrative cadence.
- **Kinetic Karaoke Subtitles**: Word-by-word active golden yellow highlights (`\c&H0000E6FF&`) against white text with thick black borders, timed to millisecond precision with `faster-whisper`.
- **Procedural Lo-Fi Backing Track**: Atmospheric ambient chord progression synthesized in pure Python with subtle vinyl crackle and kick heartbeat.

---

## 🏗️ Architecture & Project Structure

```
book-2min/
├── .env.example              # Environment variables template
├── .gitignore                # Production ignore rules (excludes large media/logs)
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── main.py                   # Unified CLI runner for all pipeline stages
│
├── src/                      # Modular Python package
│   ├── __init__.py           # Package exports
│   ├── config.py             # Global constants, paths, and subtitle styling
│   ├── script_generator.py   # 5-Beat viral non-fiction hook framework
│   ├── prompt_engine.py      # StickLit prompt builder (The Everyman formula)
│   ├── tts_engine.py         # Deepgram Aura-2 Thalia & Edge-TTS synthesis
│   ├── speech_aligner.py     # Faster-Whisper word-level timestamp alignment
│   ├── subtitle_generator.py # ASS karaoke generator with active word highlighting
│   ├── audio_mixer.py        # Procedural Lo-Fi music synthesizer
│   └── video_renderer.py     # Native FFmpeg 9:16 video assembly engine
│
└── examples/
    └── rich_dad_poor_dad/    # Complete reference dataset
        ├── metadata.json     # Production specs, pacing, and scene counts
        ├── script.txt        # Full 412-word, 147-second script
        └── prompts.json      # 40 full StickLit scene prompts
```

---

## 🎨 The StickLit Prompt Formula

All scene illustrations adhere to the strict prompt template:

```
9:16 vertical cartoon line-art illustration in the StickLit book summary style. Character design: {character_design}. {shot_type}, {focal_action}. Headline across the top: "{headline}". Callout tags: "{tag_1}", "{tag_2}". White background, thick dark ink outlines, pure 2D cartoon rendering, subtle shadow, {color_accents}. {human_clause}.
```

### Character Design: "The Everyman"
```
The Everyman, a classic black-ink stick figure wearing a crisp white collared shirt and thin black necktie
```

### Key Visual Rules:
1. **Solid White Background**: Clean, distraction-free backdrop.
2. **Thick Dark Ink Outlines**: High-contrast 2D cartoon rendering.
3. **Upper Headline Banner**: Bold distressed block capitals summarizing the core concept.
4. **Callout Tags**: Two concise micro-labels identifying components or outcomes.
5. **Selective Color Accents**: Luminous emerald green for cash/assets, crimson red for debt/liabilities/danger, royal purple for the host.

---

## 🎙️ Voiceover Engine (Deepgram Aura-2)

The pipeline integrates Deepgram's flagship conversational voice model:
- **Model**: `aura-2-thalia-en`
- **Smart Chunking**: Deepgram enforces a 2,000-character payload limit per HTTP request. `src/tts_engine.py` splits long scripts into sentence-aware chunks (<1,800 characters) and concatenates audio byte streams.
- **Edge-TTS Fallback**: Automatic fallback to Microsoft Edge Neural TTS (`en-US-ChristopherNeural`) if no API key is provided.

---

## ⚡ Quickstart & Installation

### 1. Prerequisites
- Python 3.10+
- [FFmpeg](https://ffmpeg.org/download.html) installed and added to your system `PATH`.

### 2. Clone & Install Dependencies
```bash
git clone https://github.com/Etzkennyboi/book-2min.git
cd book-2min

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Configure API Credentials
Copy `.env.example` to `.env` and insert your Deepgram API key:
```bash
cp .env.example .env
```
In `.env`:
```env
DEEPGRAM_API_KEY=your_deepgram_api_key_here
DEEPGRAM_VOICE_MODEL=aura-2-thalia-en
```

---

## 💻 CLI Usage

The CLI (`main.py`) exposes modular commands for each stage or a single one-step command:

### 1. Generate StickLit Prompts for a Book
```bash
python main.py prompts --book "Rich Dad Poor Dad" --output output/prompts.json
```

### 2. Synthesize Voiceover
```bash
python main.py voiceover --script examples/rich_dad_poor_dad/script.txt --provider deepgram --output output/voiceover.mp3
```

### 3. Extract Word-Level Timestamps with Whisper
```bash
python main.py align --audio output/voiceover.mp3 --output output/timestamps.json
```

### 4. Generate Kinetic Karaoke Subtitles
```bash
python main.py subtitles --timestamps output/timestamps.json --output output/subtitles.ass
```

### 5. Synthesize Procedural Lo-Fi BGM
```bash
python main.py bgm --duration 147.26 --output output/bgm.wav
```

### 6. Render 9:16 Master Video
```bash
python main.py render \
  --images-dir path/to/scene_images/ \
  --voiceover output/voiceover.mp3 \
  --subtitles output/subtitles.ass \
  --duration 147.26 \
  --output output/rich_dad_poor_dad_master.mp4
```

### 7. Run Full Pipeline End-to-End
```bash
python main.py pipeline \
  --book "Rich Dad Poor Dad" \
  --images-dir path/to/scene_images/ \
  --script examples/rich_dad_poor_dad/script.txt \
  --provider deepgram \
  --output output/rich_dad_poor_dad_master.mp4
```

---

## 📊 Reference Case Study: *Rich Dad Poor Dad*

The included reference production demonstrates the complete output specifications:

| Metric | Specification |
| :--- | :--- |
| **Duration** | 147.26 seconds (2 mins 27 secs) |
| **Scenes** | 40 full-frame illustrations |
| **Pacing** | 3.68 seconds per visual cut |
| **Resolution** | 1080 x 1920 (9:16 Vertical Video) |
| **Frame Rate** | 30 FPS |
| **Voiceover** | Deepgram Aura-2 Thalia (`aura-2-thalia-en`) |
| **Subtitle Style** | ASS Karaoke (Yellow Active Word, White Inactive, Black Outline) |
| **Audio Mix** | Voiceover + Lo-Fi backing track with automated ducking |

---

## 🤝 Contributing

Contributions and PRs are welcome! Feel free to add support for new AI image backends, expanded book framework templates, or multi-language subtitle pipelines.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
