"""
Subtitle Generator Module
Generates Advanced SubStation Alpha (.ass) subtitles with StickLit
word-by-word karaoke active-color highlights and anti-flicker smoothing.
"""

from pathlib import Path
from typing import Dict, Any, List
from .config import SUBTITLE_STYLE

def format_ass_time(seconds: float) -> str:
    """Formats seconds to ASS timestamp format H:MM:SS.cs"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def generate_karaoke_subtitles(
    align_data: Dict[str, Any],
    output_ass_path: Path,
    words_per_phrase: int = 4
) -> Path:
    """
    Creates word-by-word karaoke subtitles where the current active word
    lights up in vibrant yellow with solid black borders.
    """
    s = SUBTITLE_STYLE
    ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: StickLit,{s['font_name']},{s['font_size']},{s['primary_color']},{s['active_color']},{s['outline_color']},{s['back_color']},-1,0,0,0,100,100,1,0,1,{s['outline_width']},{s['shadow_depth']},{s['alignment']},40,40,{s['margin_v']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    events: List[str] = []
    all_words = align_data.get("words", [])

    if not all_words:
        # Fallback to segment-level text if word timestamps are missing
        for seg in align_data.get("segments", []):
            st = format_ass_time(seg["start"])
            et = format_ass_time(seg["end"])
            events.append(f"Dialogue: 0,{st},{et},StickLit,,0,0,0,,{seg['text'].upper()}")
    else:
        for i in range(0, len(all_words), words_per_phrase):
            chunk = all_words[i:i + words_per_phrase]
            
            # Anti-flicker: keep phrase visible until next phrase starts
            if i + words_per_phrase < len(all_words):
                next_start = all_words[i + words_per_phrase]["start"]
                phrase_end = min(chunk[-1]["end"] + 0.5, next_start)
            else:
                phrase_end = chunk[-1]["end"] + 1.0

            for w_idx, active_word in enumerate(chunk):
                w_start = active_word["start"]
                w_end = chunk[w_idx + 1]["start"] if w_idx + 1 < len(chunk) else phrase_end

                line_parts = []
                for j, w in enumerate(chunk):
                    clean_word = w["word"].strip().upper()
                    if j == w_idx:
                        # Active word colored with active_color (\c&H0000E6FF&)
                        line_parts.append(r"{\c" + s["active_color"] + r"}" + clean_word + r"{\c" + s["primary_color"] + r"}")
                    else:
                        line_parts.append(clean_word)

                dialogue_text = " ".join(line_parts)
                events.append(
                    f"Dialogue: 0,{format_ass_time(w_start)},{format_ass_time(w_end)},StickLit,,0,0,0,,{dialogue_text}"
                )

    output_ass_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(events) + "\n")

    print(f"[Subtitle Generator] Created karaoke ASS file with {len(events)} events at {output_ass_path}")
    return output_ass_path
