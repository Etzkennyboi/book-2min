# pipeline/ — StickLit Modular Engine

These are the internal modules that `sticklit.py` calls. You don't need to touch these directly — use `sticklit.py` commands instead.

## Modules

| Module | What it does |
| :--- | :--- |
| `config.py` | Global constants: canvas size (1080×1920), FPS (30), subtitle colors, paths |
| `tts_engine.py` | Synthesizes voiceover audio using Deepgram Aura-2 (or Edge-TTS fallback) |
| `speech_aligner.py` | Sends audio to Deepgram Nova-2 and returns word-level millisecond timestamps |
| `subtitle_generator.py` | Builds Golden Yellow ASS subtitle file from timestamps |
| `audio_mixer.py` | Ducks background music to -18.4 dB under voiceover using FFmpeg |
| `video_renderer.py` | Normalizes images → builds CFR 30fps frame sequence → encodes final MP4 |

## Modification Rules

- **config.py**: Safe to edit canvas size, FPS, or subtitle style — changes affect all books
- **tts_engine.py**: Safe to swap voice model or add new TTS providers
- **video_renderer.py**: Do not change CFR or yuv420p settings — subtitle sync depends on it
- **speech_aligner.py**: Do not change — Deepgram Nova-2 output format must stay consistent for `exact_cues.json` generation
