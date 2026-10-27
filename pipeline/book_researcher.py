"""
Book Researcher Module
Intakes a book title/author and extracts core thesis, 3-4 key principles,
and the high-impact narrative hook for a 2-minute retention video.
"""

import os
import json
import argparse

def resolve_book_dir(book_title: str) -> tuple[str, str]:
    slug = book_title.lower().replace(" ", "_").replace("'", "").replace(",", "").replace("-", "_")
    direct = os.path.join("books", slug)
    if os.path.exists(direct):
        return direct, slug
    alt = slug.removeprefix("the_")
    alt_dir = os.path.join("books", alt)
    if os.path.exists(alt_dir):
        return alt_dir, alt
    if os.path.exists("books"):
        for d in os.listdir("books"):
            full = os.path.join("books", d)
            if os.path.isdir(full):
                if d == slug or d == alt or d in slug or slug in d:
                    return full, d
    return direct, slug

class BookResearcher:
    def __init__(self, book_title: str):
        self.book_title = book_title
        self.output_dir, self.slug = resolve_book_dir(book_title)
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_research_brief(self) -> dict:
        """
        Creates a structured framework for distilling a book into a 2-minute short.
        """
        brief = {
            "title": self.book_title,
            "slug": self.slug,
            "target_duration_seconds": 120,
            "target_word_count": 280, # ~2.33 words/sec
            "structure_5_stage": {
                "stage_1_golden_hook": {
                    "duration": "0s - 15s (~35 words)",
                    "goal": "Counter-intuitive paradox or jarring reality check that grabs immediate attention."
                },
                "stage_2_disrupt_assumptions": {
                    "duration": "15s - 35s (~45 words)",
                    "goal": "Shatter conventional advice or mainstream myth the reader assumes to be true."
                },
                "stage_3_core_mechanism": {
                    "duration": "35s - 75s (~90 words)",
                    "goal": "Explain the hidden friction, psychological mechanism, or author's unique mental model."
                },
                "stage_4_actionable_truth": {
                    "duration": "75s - 105s (~70 words)",
                    "goal": "Deliver the concrete behavioral pivot or strategy to immediately apply today."
                },
                "stage_5_elevation_and_discussion": {
                    "duration": "105s - 120s (~40 words)",
                    "goal": "Punchline takeaway plus provocative discussion question driving comments."
                }
            }
        }

        brief_path = os.path.join(self.output_dir, "research_brief.json")
        with open(brief_path, "w", encoding="utf-8") as f:
            json.dump(brief, f, indent=2)

        print(f"[*] 2-Minute Book Research Brief established: {brief_path}")
        return brief

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Research and outline a book for a 2-minute video.")
    parser.add_argument("--book", required=True, help="Book title (e.g. 'Atomic Habits')")
    args = parser.parse_args()

    researcher = BookResearcher(args.book)
    researcher.generate_research_brief()
