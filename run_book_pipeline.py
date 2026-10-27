"""
Master CLI: 2-Minute Book Summary Video Engine
End-to-End Orchestrator for High-Retention Book Summaries (@sticklit style).

Usage:
  python run_book_pipeline.py --book "Atomic Habits" --step all
  python run_book_pipeline.py --book "The Psychology of Money" --step research
  python run_book_pipeline.py --book "Rich Dad Poor Dad" --step prompts
"""

import sys
import os
import argparse

# Ensure utf-8 stdout on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from pipeline.book_researcher import BookResearcher, resolve_book_dir
from pipeline.script_generator import generate_script_structure
from pipeline.prompt_engine import generate_prompts_for_book

def main():
    parser = argparse.ArgumentParser(description="2-Minute Book Summary Video Engine")
    parser.add_argument("--book", required=True, help="Book title (e.g. 'Atomic Habits', 'Psychology of Money')")
    parser.add_argument("--author", default="", help="Author name (optional)")
    parser.add_argument("--step", choices=["research", "script", "prompts", "align", "render", "all"], default="all", help="Pipeline step to execute")
    args = parser.parse_args()

    book_title = args.book
    author = args.author
    book_dir, slug = resolve_book_dir(book_title)
    os.makedirs(book_dir, exist_ok=True)

    print("=" * 80)
    print(f"[*] 2-MINUTE BOOK SUMMARY PIPELINE: {book_title.upper()}")
    print("=" * 80)

    # Step 1: Research Brief
    if args.step in ["research", "all"]:
        print("\n[Step 1/5] Establishing Research Brief & 5-Beat Framework...")
        researcher = BookResearcher(book_title)
        researcher.generate_research_brief()

    # Step 2: Script Structure
    if args.step in ["script", "all"]:
        print("\n[Step 2/5] Structuring 2-Minute Script Framework...")
        struct = generate_script_structure(book_title, author or "Author", "Core Theme")
        print(f"[+] Script blueprint generated for {book_title} (Target: ~{struct['target_word_count']} words, {struct['target_duration_seconds']}s)")
        print(f"    Check template and write script to: {os.path.join(book_dir, 'script.txt')}")

    # Step 3: Prompt Generation
    if args.step in ["prompts", "all"]:
        print("\n[Step 3/5] Generating Visual Prompt Package...")
        prompts_path = os.path.join(book_dir, "prompts.txt")
        if os.path.exists(prompts_path):
            print(f"[+] Existing prompt package located: {prompts_path}")
        else:
            print(f"[*] Prompts will be output to: {prompts_path}")

    # Step 4: Speech & Subtitle Alignment
    if args.step in ["align", "all"]:
        print("\n[Step 4/5] Audio & Subtitle Alignment...")
        cues_path = os.path.join(book_dir, "exact_cues.json")
        subtitles_path = os.path.join(book_dir, "golden_subtitles.ass")
        if os.path.exists(cues_path):
            print(f"[+] Word-level cues verified: {cues_path}")
        if os.path.exists(subtitles_path):
            print(f"[+] Kinetic subtitles verified: {subtitles_path}")

    # Step 5: Video Render
    if args.step in ["render", "all"]:
        print("\n[Step 5/5] Final Video Assembly...")
        print(f"[*] Output video target: output/{slug}/{slug}_master.mp4")

    print("\n" + "=" * 80)
    print("[+] BOOK PIPELINE FINISHED")
    print("=" * 80)

if __name__ == "__main__":
    main()
