"""
StickLit Prompt Engine
Generates 9:16 vertical cartoon line-art prompts with The Everyman character,
bold headline banners, and visual callout tags.
"""

from typing import List, Dict, Any

PROMPT_TEMPLATE = (
    "9:16 vertical cartoon line-art illustration in the StickLit book summary style. "
    "Character design: {character_design}. "
    "{shot_type}, {focal_action}. "
    'Headline across the top: "{headline}". '
    'Callout tags: "{tag_1}", "{tag_2}". '
    "White background, thick dark ink outlines, pure 2D cartoon rendering, subtle shadow, "
    "{color_accents}. {human_clause}."
)

DEFAULT_EVERYMAN = (
    "The Everyman, a classic black-ink stick figure wearing a crisp white collared shirt "
    "and thin black necktie"
)

def build_scene_prompt(
    headline: str,
    focal_action: str,
    tag_1: str,
    tag_2: str,
    shot_type: str = "Wide shot",
    character_design: str = DEFAULT_EVERYMAN,
    color_accents: str = "emerald green cash, dark metallic accents",
    human_clause: str = "The Everyman is the only human character"
) -> str:
    """
    Builds a single StickLit image prompt following the master formula.
    """
    return PROMPT_TEMPLATE.format(
        character_design=character_design,
        shot_type=shot_type,
        focal_action=focal_action,
        headline=headline,
        tag_1=tag_1,
        tag_2=tag_2,
        color_accents=color_accents,
        human_clause=human_clause
    )

def generate_book_prompts(scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Converts a list of scene descriptions into ready-to-run StickLit image prompts.
    """
    results = []
    for idx, sc in enumerate(scenes, 1):
        prompt = build_scene_prompt(
            headline=sc.get("headline", f"SCENE {idx}"),
            focal_action=sc.get("action", ""),
            tag_1=sc.get("tag_1", "KEY CONCEPT"),
            tag_2=sc.get("tag_2", "TAKEAWAY"),
            shot_type=sc.get("shot_type", "Wide shot"),
            character_design=sc.get("character_design", DEFAULT_EVERYMAN),
            color_accents=sc.get("color_accents", "subtle color accents"),
            human_clause=sc.get("human_clause", "The Everyman is the only human character")
        )
        results.append({
            "scene_number": idx,
            "filename": f"scene_{idx:03d}.png",
            "headline": sc.get("headline"),
            "prompt": prompt
        })
    return results
