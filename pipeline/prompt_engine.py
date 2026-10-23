"""
StickLit Master Prompt Engine (v2.1)
====================================
Generates viral, high-retention 9:16 vertical 2D stick-figure image prompts
in the signature @sticklit webcomic style on a pure white (#FFFFFF) background.

Features:
- Mandatory Scene 01 Intentional Viral Hook Architecture (0.2s scroll-stopping thumbnail).
- Locked Canonical Protagonist Duo (Kai & Maya) with flat warm skin tone and 2D stick limbs.
- Scene 01 Zero-Tilt Colossal Upright Book Standard (zero neck bending).
- Scene Last Single Cohesive Horizontal Split-Screen Dilemma ((VS) badge).
- 250px Subtitle Safety Zone Enforcement.
"""

from typing import List, Dict, Any, Optional

STICKLIT_MASTER_PREFIX = (
    "9:16 vertical 2D minimalist cartoon stick-figure illustration in the exact @sticklit style. "
    "Pure borderless white background (#FFFFFF) with abundant clean negative space. "
    "Crisp solid black ink outlines, flat solid color fills, zero 3D rendering, zero gradients, "
    "zero background clutter, no floor planes, no wall textures. Near the top center, small subtle text: '@sticklit'."
)

LOCKED_KAI = (
    "Kai (Boy stick figure, circular head with flat warm natural skin tone, messy spiky jet-black hair, "
    "dark charcoal short-sleeve crewneck tee #3A3A3C, medium grey straight trousers #8E8E93, black combat boots, "
    "expressive black comic eyes, arched eyebrows, confident knowing smirk, minimalist 2D black stick limbs with strictly zero muscular bulk)"
)

LOCKED_MAYA = (
    "Maya (Girl stick figure, circular head with flat warm natural skin tone, high energetic spiky jet-black ponytail with fringe bangs, "
    "dark charcoal short-sleeve fitted crewneck tee #3A3A3C, medium grey straight trousers #8E8E93, black combat boots, "
    "expressive black comic eyes, arched eyebrows, analytical wink and clever smile, minimalist 2D black stick limbs with strictly zero muscular bulk)"
)

SUBTITLE_SAFETY_DIRECTIVE = (
    "Keep all character artwork, props, and action strictly in the upper 80% of the canvas; "
    "leave the bottom 250px completely clear pure white (#FFFFFF) negative space for subtitles."
)

NEGATIVE_DIRECTIVES = (
    "(defined muscles, thick muscular limbs, realistic human anatomy, 3D render, dark background, "
    "borders, gradients, floor textures, wall textures, cut off heads, tilted book covers)"
)

# ---------------------------------------------------------------------------
# SCENE 01: INTENTIONAL VIRAL HOOK & THUMBNAIL LOGIC
# ---------------------------------------------------------------------------

HOOK_ARCHETYPES = {
    "paradox_shock": {
        "name": "The Impossible Shock Paradox",
        "description": "High-contrast juxtaposition showing humble quiet wealth triumphing over arrogant bankrupt status.",
        "default_bubble": "How a Janitor Beat Wall Street!",
        "kai_action": (
            "Leaning coolly with one arm over a simple wooden broom, casually resting his other hand on a massive, "
            "glowing transparent bank vault packed with EIGHT MILLION DOLLARS ($8,000,000) in solid gold bullion bars, "
            "looking directly into the camera with an effortless, knowing smirk."
        ),
        "maya_action": (
            "Pointing down in mocking analysis at a tiny, panicked stickman in a shredded business suit whose head "
            "is buried under a collapsing avalanche of unpaid luxury bills, foreclosure notices, and a smoking wrecked sports car."
        ),
        "props": "Transparent $8M bullion safe, broom, burning miniature supercar, scattered debt envelopes."
    },
    "kinetic_catharsis": {
        "name": "Shattering The Golden Handcuffs",
        "description": "Explosive combat action showing the violent destruction of consumer debt shackles to claim sovereignty.",
        "default_bubble": "Escape The Golden Handcuffs!",
        "kai_action": (
            "Mid-swing in an explosive combat pose, wielding a glowing golden battleaxe labeled 'SAVING' with both hands, "
            "violently SHATTERING a massive set of glowing 'GOLDEN HANDCUFFS' into flying metallic shards, breaking free "
            "from a spinning hamster wheel labeled 'DEBT'."
        ),
        "maya_action": (
            "Standing proudly atop a solid pyramid of gold bullion bars, holding high a giant glowing golden master key "
            "labeled 'TIME FREEDOM' that shoots brilliant rays of light upward, giving a sharp, victorious 4th-wall wink."
        ),
        "props": "Golden battleaxe, shattered golden handcuffs, debt hamster wheel, gold pyramid, key of time freedom."
    },
    "exponential_scale": {
        "name": "Surfing The Compounding Tsunami",
        "description": "Colossal physical scale translating compounding math into an unstoppable tidal wave of wealth.",
        "default_bubble": "Compounding Is My Superpower!",
        "kai_action": (
            "Wearing cool dark sunglasses, surfing triumphantly on the crest of a GIGANTIC, COLOSSAL curling tidal wave "
            "of sparkling gold coins and green bills surging forward: 'Compounding is my superpower.'"
        ),
        "maya_action": (
            "Standing beside the book holding an oversized glowing golden pocket watch / timer of Time, smiling knowingly "
            "at the exponential growth curve."
        ),
        "props": "Massive curling golden wave, sunglasses, giant glowing stopwatch, panicked 'Day Trader' running in corner."
    }
}


def build_scene_01_hook_prompt(
    book_title: str,
    author: str,
    hook_archetype: str = "paradox_shock",
    hook_speech_bubble: Optional[str] = None,
    kai_action: Optional[str] = None,
    maya_action: Optional[str] = None,
    book_color_scheme: str = "dark navy-blue and gold",
    book_tagline: str = "in two minutes"
) -> str:
    """
    Builds the definitive Scene 01 / Opening Hook / Thumbnail prompt.
    Enforces zero-tilt upright book, the canonical duo, active narrative conflict,
    and subtitle safety clearance.
    """
    archetype = HOOK_ARCHETYPES.get(hook_archetype, HOOK_ARCHETYPES["paradox_shock"])
    speech_bubble = hook_speech_bubble or archetype["default_bubble"]
    kai_pose = kai_action or archetype["kai_action"]
    maya_pose = maya_action or archetype["maya_action"]

    prompt_lines = [
        "[SCENE_01] " + STICKLIT_MASTER_PREFIX,
        "",
        "CRITICAL MANDATE - ZERO TILT & ZERO NECK BENDING:",
        "The book must stand PERFECTLY CENTERED, 100% upright, flat-facing the camera, level and straight. "
        "The title text MUST be 100% horizontal and effortlessly readable with zero tilt!",
        "",
        "1. Centered Book (Centerpiece):",
        f"   - A colossal, towering hardcover book planted squarely in the center of the frame, 100% upright and level.",
        f"   - Elegant {book_color_scheme} hardcover with bold, perfectly horizontal gold embossed title:",
        f'     "{book_title.upper()}"',
        f'     "{author.upper()}"',
        "   - Subtle glowing golden electric sparks crackle around the book's outer perimeter.",
        "",
        "2. High-Drama Narrative Action & Core Book Paradox Conflict:",
        f"   - LEFT SIDE: {LOCKED_KAI}",
        f"     ACTION: {kai_pose}",
        f"   - RIGHT SIDE: {LOCKED_MAYA}",
        f"     ACTION: {maya_pose}",
        f'   - TOP VIRAL HOOK BUBBLE: A bold, comic speech bubble / headline banner reading: "{speech_bubble}"',
        "",
        "3. Top Comic Header:",
        "   - Centered near top edge: subtle outline watermark '@sticklit'.",
        "   - Just below watermark, bold handwritten comic header:",
        f'     "{book_title}"',
        f'     "{author}"',
        f'     "{book_tagline}"',
        "",
        "Visual & Framing Constraints:",
        f"- Subtitle Safety: {SUBTITLE_SAFETY_DIRECTIVE}",
        f"- Negative Directives: {NEGATIVE_DIRECTIVES}"
    ]

    return "\n".join(prompt_lines)


# ---------------------------------------------------------------------------
# SCENE LAST: COHESIVE HORIZONTAL SPLIT SCREEN PROMPT
# ---------------------------------------------------------------------------

def build_scene_last_split_prompt(
    book_title: str,
    dilemma_question: str,
    top_scenario: str,
    bottom_scenario: str
) -> str:
    """
    Builds the definitive final scene binary dilemma prompt.
    Enforces a single cohesive 9:16 horizontal split screen with a central (VS) badge.
    """
    prompt_lines = [
        "[SCENE_LAST] " + STICKLIT_MASTER_PREFIX,
        "",
        "CRITICAL MANDATE - SINGLE COHESIVE HORIZONTAL SPLIT SCREEN:",
        "Generate as ONE single 9:16 vertical image divided across the center by a crisp horizontal black line "
        "with a bold circular '(VS)' badge in the middle. Do NOT generate two separate images.",
        "",
        f'1. The Final Dilemma Question: "{dilemma_question}"',
        "",
        "2. TOP PANEL (Choice A - Trapped / Costly Trap):",
        f"   {top_scenario}",
        "",
        "3. BOTTOM PANEL (Choice B - True Freedom / Sovereign Path):",
        f"   {bottom_scenario}",
        "",
        "4. Central Badge:",
        "   A prominent circular comic badge centered on the divider line labeled '(VS)' in bold punch font.",
        "",
        "Visual & Framing Constraints:",
        f"- Subtitle Safety: {SUBTITLE_SAFETY_DIRECTIVE}",
        f"- Negative Directives: {NEGATIVE_DIRECTIVES}"
    ]
    return "\n".join(prompt_lines)


# ---------------------------------------------------------------------------
# NARRATIVE SCENE PROMPT (SCENES 02 TO N-1)
# ---------------------------------------------------------------------------

def build_narrative_scene_prompt(
    scene_id: int,
    script_beat: str,
    visual_action: str,
    featured_character: str = "both",
    symbolic_props: str = "None"
) -> str:
    """
    Builds an organic narrative scene prompt (scenes 02 to N-1).
    """
    char_desc = ""
    if featured_character == "kai":
        char_desc = f"Main Character: {LOCKED_KAI}."
    elif featured_character == "maya":
        char_desc = f"Main Character: {LOCKED_MAYA}."
    elif featured_character == "both":
        char_desc = f"Protagonist Duo: {LOCKED_KAI} and {LOCKED_MAYA} acting together."
    else:
        char_desc = "Minimalist 2D stickman in charcoal tee #3A3A3C, flat warm skin tone."

    prompt_lines = [
        f"[SCENE_{scene_id:02d}] " + STICKLIT_MASTER_PREFIX,
        f'Script Context: "{script_beat}"',
        "",
        f"Visual Action: {visual_action}",
        char_desc,
        f"Symbolic Props: {symbolic_props}",
        "",
        "Framing & Style:",
        f"- Subtitle Safety: {SUBTITLE_SAFETY_DIRECTIVE}",
        f"- Negative Directives: {NEGATIVE_DIRECTIVES}"
    ]
    return "\n".join(prompt_lines)


# Backward compatibility aliases
build_scene_prompt = build_narrative_scene_prompt
