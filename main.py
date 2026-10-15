#!/usr/bin/env python3
"""
Book-2Min: High-Retention StickLit Animated Book Summary Video Generator

End-to-end pipeline:
1. Script & Prompt Generation (StickLit 5-Beat Framework & Everyman Prompt Engine)
2. High-Fidelity TTS Voiceover (Deepgram Aura-2 Thalia or Edge-TTS)
3. Speech-to-Word Alignment (faster-whisper)
4. Kinetic Karaoke Subtitles (.ass format with active word highlighting)
5. Ambient Lo-Fi Background Music Generation (pure NumPy/Wave)
6. Full 9:16 Vertical Video Assembly via native FFmpeg
"""

import sys
import argparse
from pathlib import Path
import json

from src.config import (
    BASE_DIR,
    OUTPUT_DIR,
    DEEPGRAM_API_KEY,
    DEFAULT_DEEPGRAM_MODEL,
    DEFAULT_EDGE_VOICE,
    SUBTITLE_STYLE
)
from src.script_generator import generate_script_structure, NON_FICTION_FRAMEWORK
from src.prompt_engine import generate_book_prompts, build_scene_prompt
from src.tts_engine import generate_voiceover, synthesize_deepgram, synthesize_edge_tts
from src.speech_aligner import align_speech
from src.subtitle_generator import generate_karaoke_subtitles
from src.audio_mixer import synthesize_lofi_track
from src.video_renderer import render_video


def cmd_prompts(args):
    """Generates StickLit prompts JSON for an array of scenes or book framework."""
    print(f"\n=== Generating StickLit Image Prompts for '{args.book}' ===")
    
    if args.scenes_json and Path(args.scenes_json).exists():
        with open(args.scenes_json, "r", encoding="utf-8") as f:
            scenes = json.load(f)
    else:
        # Load sample scenes if not provided
        sample_path = BASE_DIR / "examples" / "rich_dad_poor_dad" / "scenes.json"
        if sample_path.exists():
            with open(sample_path, "r", encoding="utf-8") as f:
                scenes = json.load(f)
        else:
            print("No scenes provided; creating sample 5-scene structure.")
            scenes = [
                {
                    "headline": "THE RAT RACE",
                    "action": "Inside a giant circular wire hamster wheel, an exhausted The Everyman sprints furiously, head thrown back and cyan sweat drops flying",
                    "tag_1": "ENDLESS TRAP",
                    "tag_2": "ZERO PROGRESS",
                    "shot_type": "Wide shot",
                    "color_accents": "cyan sweat drops, distressed red sign"
                },
                {
                    "headline": "TWO DADS, TWO PATHS",
                    "action": "A large central fork in the road. On the left, a diploma and stacks of bills; on the right, asset deeds and rental properties",
                    "tag_1": "POOR DAD",
                    "tag_2": "RICH DAD",
                    "shot_type": "Wide shot",
                    "color_accents": "emerald green deeds, crimson bills"
                }
            ]

    prompts = generate_book_prompts(scenes)
    out_file = Path(args.output) if args.output else OUTPUT_DIR / f"{args.book.lower().replace(' ', '_')}_prompts.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(prompts)} StickLit prompts saved to: {out_file}")
    if prompts:
        print("\n--- Example Generated Prompt (Scene 1) ---")
        print(prompts[0]["prompt"])


def cmd_voiceover(args):
    """Generates voiceover using Deepgram Aura-2 or Edge-TTS."""
    print(f"\n=== Generating Voiceover ({args.provider.upper()}) ===")
    script_path = Path(args.script)
    if not script_path.exists():
        raise FileNotFoundError(f"Script file not found: {script_path}")

    with open(script_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    out_file = Path(args.output) if args.output else OUTPUT_DIR / "voiceover.mp3"
    generate_voiceover(text, out_file, provider=args.provider, deepgram_key=args.deepgram_key)
    print(f"Voiceover successfully generated: {out_file}")


def cmd_align(args):
    """Aligns speech to extract word-level timestamps using faster-whisper."""
    print(f"\n=== Aligning Speech with Faster-Whisper ===")
    audio_path = Path(args.audio)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    out_file = Path(args.output) if args.output else OUTPUT_DIR / "timestamps.json"
    align_speech(audio_path, out_file, model_size=args.model_size)
    print(f"Word timestamps saved to: {out_file}")


def cmd_subtitles(args):
    """Generates kinetic karaoke .ass subtitles from timestamp JSON."""
    print(f"\n=== Generating Kinetic Karaoke Subtitles ===")
    timestamps_path = Path(args.timestamps)
    if not timestamps_path.exists():
        raise FileNotFoundError(f"Timestamps file not found: {timestamps_path}")

    with open(timestamps_path, "r", encoding="utf-8") as f:
        align_data = json.load(f)

    out_file = Path(args.output) if args.output else OUTPUT_DIR / "subtitles.ass"
    generate_karaoke_subtitles(align_data, out_file, words_per_phrase=args.words_per_phrase)
    print(f"Karaoke subtitles saved to: {out_file}")


def cmd_bgm(args):
    """Synthesizes an ambient Lo-Fi backing track."""
    print(f"\n=== Synthesizing Lo-Fi Backing Track ({args.duration}s) ===")
    out_file = Path(args.output) if args.output else OUTPUT_DIR / "bgm.wav"
    synthesize_lofi_track(args.duration, out_file)
    print(f"Lo-Fi track saved to: {out_file}")


def cmd_render(args):
    """Renders final video from images, voiceover, bgm, and subtitles."""
    print(f"\n=== Rendering 9:16 Master Video ===")
    images_dir = Path(args.images_dir)
    if not images_dir.is_dir():
        raise NotADirectoryError(f"Images directory not found: {images_dir}")

    # Collect images sorted by name
    valid_exts = {".png", ".jpg", ".jpeg", ".webp"}
    images = sorted([f for f in images_dir.iterdir() if f.suffix.lower() in valid_exts])
    if not images:
        raise ValueError(f"No valid images found in: {images_dir}")

    voiceover = Path(args.voiceover)
    subtitles = Path(args.subtitles)
    
    # Optional bgm
    if args.bgm and Path(args.bgm).exists():
        bgm_path = Path(args.bgm)
    else:
        # Synthesize on the fly
        bgm_path = OUTPUT_DIR / "bgm_temp.wav"
        synthesize_lofi_track(args.duration, bgm_path)

    out_file = Path(args.output) if args.output else OUTPUT_DIR / "final_book_summary.mp4"
    render_video(
        image_paths=images,
        voiceover_path=voiceover,
        bgm_path=bgm_path,
        subtitles_path=subtitles,
        duration=args.duration,
        output_video_path=out_file,
        bgm_volume=args.bgm_volume
    )


def cmd_pipeline(args):
    """Runs the full end-to-end pipeline."""
    print(f"\n=======================================================")
    print(f"   Book-2Min: Full Automated Production Pipeline")
    print(f"=======================================================")

    images_dir = Path(args.images_dir)
    if not images_dir.is_dir():
        raise NotADirectoryError(f"Images directory not found: {images_dir}")

    script_path = Path(args.script)
    if not script_path.exists():
        raise FileNotFoundError(f"Script file not found: {script_path}")

    valid_exts = {".png", ".jpg", ".jpeg", ".webp"}
    images = sorted([f for f in images_dir.iterdir() if f.suffix.lower() in valid_exts])
    print(f"[Pipeline] Found {len(images)} scene images in {images_dir}")

    with open(script_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    # Step 1: Voiceover
    vo_path = OUTPUT_DIR / "pipeline_voiceover.mp3"
    generate_voiceover(text, vo_path, provider=args.provider, deepgram_key=args.deepgram_key)

    # Step 2: Speech Alignment
    align_path = OUTPUT_DIR / "pipeline_timestamps.json"
    align_data = align_speech(vo_path, align_path)
    duration = align_data["duration"]

    # Step 3: Subtitles
    ass_path = OUTPUT_DIR / "pipeline_subtitles.ass"
    generate_karaoke_subtitles(align_data, ass_path)

    # Step 4: Lo-Fi BGM
    bgm_path = OUTPUT_DIR / "pipeline_bgm.wav"
    synthesize_lofi_track(duration, bgm_path)

    # Step 5: Master Render
    out_video = Path(args.output) if args.output else OUTPUT_DIR / f"{args.book.lower().replace(' ', '_')}_master.mp4"
    render_video(
        image_paths=images,
        voiceover_path=vo_path,
        bgm_path=bgm_path,
        subtitles_path=ass_path,
        duration=duration,
        output_video_path=out_video
    )

    print(f"\n🎉 ALL STEPS COMPLETED!")
    print(f"Final Master Video ready at: {out_video.resolve()}")


def main():
    parser = argparse.ArgumentParser(
        description="Book-2Min: Automated 2-Minute High-Retention Book Summary Video Generator"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Subcommand: prompts
    p_prompts = subparsers.add_parser("prompts", help="Generate StickLit image prompts")
    p_prompts.add_argument("--book", default="Rich Dad Poor Dad", help="Book title")
    p_prompts.add_argument("--scenes-json", help="Path to scenes JSON input")
    p_prompts.add_argument("--output", help="Output JSON path for prompts")
    p_prompts.set_defaults(func=cmd_prompts)

    # Subcommand: voiceover
    p_vo = subparsers.add_parser("voiceover", help="Generate voiceover speech")
    p_vo.add_argument("--script", required=True, help="Path to script text file")
    p_vo.add_argument("--provider", default="deepgram", choices=["deepgram", "edge"], help="TTS provider")
    p_vo.add_argument("--deepgram-key", help="Deepgram API key override")
    p_vo.add_argument("--output", help="Output MP3 file path")
    p_vo.set_defaults(func=cmd_voiceover)

    # Subcommand: align
    p_align = subparsers.add_parser("align", help="Align voiceover audio into word timestamps")
    p_align.add_argument("--audio", required=True, help="Audio file path")
    p_align.add_argument("--model-size", default="base.en", help="Whisper model size")
    p_align.add_argument("--output", help="Output JSON timestamps path")
    p_align.set_defaults(func=cmd_align)

    # Subcommand: subtitles
    p_sub = subparsers.add_parser("subtitles", help="Generate kinetic karaoke ASS subtitles")
    p_sub.add_argument("--timestamps", required=True, help="Timestamps JSON path")
    p_sub.add_argument("--words-per-phrase", type=int, default=4, help="Words per karaoke line")
    p_sub.add_argument("--output", help="Output ASS subtitle file path")
    p_sub.set_defaults(func=cmd_subtitles)

    # Subcommand: bgm
    p_bgm = subparsers.add_parser("bgm", help="Synthesize Lo-Fi background music")
    p_bgm.add_argument("--duration", type=float, required=True, help="Duration in seconds")
    p_bgm.add_argument("--output", help="Output WAV path")
    p_bgm.set_defaults(func=cmd_bgm)

    # Subcommand: render
    p_render = subparsers.add_parser("render", help="Render final video with FFmpeg")
    p_render.add_argument("--images-dir", required=True, help="Folder containing scene images")
    p_render.add_argument("--voiceover", required=True, help="Voiceover audio path")
    p_render.add_argument("--subtitles", required=True, help="Karaoke ASS subtitle path")
    p_render.add_argument("--duration", type=float, required=True, help="Total duration in seconds")
    p_render.add_argument("--bgm", help="Optional BGM audio path")
    p_render.add_argument("--bgm-volume", type=float, default=0.15, help="BGM volume factor")
    p_render.add_argument("--output", help="Output MP4 video path")
    p_render.set_defaults(func=cmd_render)

    # Subcommand: pipeline
    p_pipe = subparsers.add_parser("pipeline", help="Run complete end-to-end pipeline")
    p_pipe.add_argument("--book", default="Rich Dad Poor Dad", help="Book title")
    p_pipe.add_argument("--images-dir", required=True, help="Folder containing ordered scene images")
    p_pipe.add_argument("--script", required=True, help="Script text file")
    p_pipe.add_argument("--provider", default="deepgram", choices=["deepgram", "edge"], help="TTS provider")
    p_pipe.add_argument("--deepgram-key", help="Deepgram API key override")
    p_pipe.add_argument("--output", help="Output MP4 path")
    p_pipe.set_defaults(func=cmd_pipeline)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
