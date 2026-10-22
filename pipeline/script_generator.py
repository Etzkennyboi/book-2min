"""
Script Generator Module for 2-Minute Book Summaries
Implements the 5-Beat Viral Hook & Retention Framework used by @sticklit.
"""

from typing import Dict, Any

NON_FICTION_FRAMEWORK = """
[BEAT 1: THE HOOK & PARADOX] (0:00 - 0:15)
- Opening: "{book_title} by {author} in two minutes."
- The Provocative Paradox: The counter-intuitive question that exposes a common flawed human behavior.
- The Core Premise: Why conventional advice fails and what the book actually addresses.

[BEAT 2: THE CONTRAST / TWO PATHS] (0:15 - 0:45)
- Contrast two opposing characters, mindsets, or historical strategies (e.g., Poor Dad vs. Rich Dad, Goals vs. Systems, Inclusive vs. Extractive).
- Show the fatal flaw of the conventional path.

[BEAT 3: THE CORE FRAMEWORK] (0:45 - 1:20)
- The author's primary 2-part model or mental shift (e.g., Assets vs. Liabilities, Let Them vs. Let Me).
- Concrete definitions with tangible physical metaphors.

[BEAT 4: THE ESCALATION & TRAP] (1:20 - 1:55)
- The behavioral trap (e.g., The Rat Race, Lifestyle Inflation, The Need for Certainty).
- Why smart people stay stuck even when they try hard.

[BEAT 5: THE PHILOSOPHICAL REFRAME] (1:55 - 2:25)
- The practical solution: Cash flow, compounding, letting go.
- The closing memorable quote/question: "The moment you say you can't afford it, your brain stops thinking. But when you ask how you can, your mind goes to work."
"""

def generate_script_structure(book_title: str, author: str, core_theme: str) -> Dict[str, Any]:
    """
    Returns structured blueprint metadata for writing a high-retention 2-minute script.
    """
    return {
        "book_title": book_title,
        "author": author,
        "core_theme": core_theme,
        "target_duration_seconds": 145,
        "target_word_count": 360,
        "target_wpm": 150,
        "beats": [
            {"id": 1, "name": "Hook & Paradox", "duration_sec": 15},
            {"id": 2, "name": "The Contrast / Two Paths", "duration_sec": 30},
            {"id": 3, "name": "The Core Framework", "duration_sec": 35},
            {"id": 4, "name": "The Trap & Escalation", "duration_sec": 35},
            {"id": 5, "name": "The Philosophical Synthesis", "duration_sec": 30}
        ],
        "framework_prompt": NON_FICTION_FRAMEWORK.format(book_title=book_title, author=author)
    }
