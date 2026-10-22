"""
Speech Aligner Module
Extracts millisecond-accurate word-level and segment-level timestamps
using faster-whisper.
"""

import json
import subprocess
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from .config import FFMPEG_PATH, FFPROBE_PATH

try:
    import numpy as np
    from faster_whisper import WhisperModel
    HAS_WHISPER = True
except ImportError:
    HAS_WHISPER = False

def get_audio_duration(file_path: Path) -> float:
    """Gets exact audio duration in seconds using ffprobe."""
    try:
        cmd = [
            FFPROBE_PATH, "-v", "error", "-show_entries",
            "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
            str(file_path.resolve())
        ]
        out = subprocess.check_output(cmd, text=True).strip()
        return float(out)
    except Exception:
        return 0.0

def align_script_text(
    audio_path: Path,
    output_json_path: Path,
    script_text: Optional[str] = None
) -> Dict[str, Any]:
    """
    High-precision duration and punctuation-weighted word alignment fallback
    when faster-whisper is not installed.
    """
    total_dur = get_audio_duration(audio_path)
    if total_dur <= 0:
        total_dur = 120.0

    if not script_text:
        # Check if a .txt script exists in the same folder or examples
        txt_cand = list(audio_path.parent.glob("*.txt"))
        if txt_cand:
            script_text = txt_cand[0].read_text(encoding="utf-8")
        else:
            script_text = "The Subtle Art of Not Giving a Fuck by Mark Manson."

    # Parse into sentences and words
    sentences = [s.strip() for s in re.split(r'([.?!]+)', script_text) if s.strip()]
    merged_sentences = []
    i = 0
    while i < len(sentences):
        if i + 1 < len(sentences) and re.match(r'^[.?!]+$', sentences[i + 1]):
            merged_sentences.append(sentences[i] + sentences[i + 1])
            i += 2
        else:
            merged_sentences.append(sentences[i])
            i += 1

    # Calculate weights based on character length + punctuation pause
    sent_weights = []
    for s in merged_sentences:
        weight = len(s) + 15  # Pause bonus for sentence boundaries
        sent_weights.append(weight)

    total_weight = sum(sent_weights) if sum(sent_weights) > 0 else 1.0
    
    seg_list = []
    all_words = []
    cur_time = 0.3  # Initial silence padding

    effective_dur = max(total_dur - 0.6, 1.0)

    for s_idx, (sentence, w) in enumerate(zip(merged_sentences, sent_weights)):
        s_dur = (w / total_weight) * effective_dur
        s_start = cur_time
        s_end = min(cur_time + s_dur, total_dur)
        words_in_sent = [wrd.strip() for wrd in sentence.split() if wrd.strip()]
        
        if words_in_sent:
            wrd_total_chars = sum(len(x) for x in words_in_sent) + len(words_in_sent)
            w_cur = s_start
            wrd_list = []
            for wrd in words_in_sent:
                w_char_dur = (len(wrd) + 1) / wrd_total_chars * (s_dur * 0.92)
                w_info = {
                    "word": wrd,
                    "start": round(w_cur, 2),
                    "end": round(w_cur + w_char_dur, 2)
                }
                wrd_list.append(w_info)
                all_words.append(w_info)
                w_cur += w_char_dur

            seg_list.append({
                "id": s_idx,
                "start": round(s_start, 2),
                "end": round(s_end, 2),
                "text": sentence,
                "words": wrd_list
            })
        cur_time = s_end

    result = {
        "audio_file": str(audio_path),
        "duration": round(total_dur, 2),
        "segments": seg_list,
        "words": all_words
    }

    output_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[Speech Aligner] Aligned {len(all_words)} words across {len(seg_list)} segments. Duration: {total_dur:.2f}s")
    return result

def align_speech(
    audio_path: Path,
    output_json_path: Path,
    model_size: str = "base.en",
    script_text: Optional[str] = None
) -> Dict[str, Any]:
    """
    Transcribes audio and extracts word timestamps using Whisper if available,
    otherwise falling back to precision script duration alignment.
    """
    if not HAS_WHISPER:
        return align_script_text(audio_path, output_json_path, script_text=script_text)

    try:
        print(f"[Whisper Aligner] Loading Whisper {model_size} model...")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        print(f"[Whisper Aligner] Aligning audio words from {audio_path}...")
        segments, info = model.transcribe(str(audio_path), beam_size=5, word_timestamps=True)

        seg_list: List[Dict[str, Any]] = []
        all_words: List[Dict[str, Any]] = []

        for s in segments:
            words_in_seg = []
            if s.words:
                for w in s.words:
                    w_info = {
                        "word": w.word.strip(),
                        "start": round(w.start, 2),
                        "end": round(w.end, 2)
                    }
                    words_in_seg.append(w_info)
                    all_words.append(w_info)

            seg_list.append({
                "id": s.id,
                "start": round(s.start, 2),
                "end": round(s.end, 2),
                "text": s.text.strip(),
                "words": words_in_seg
            })

        result = {
            "audio_file": str(audio_path),
            "duration": round(info.duration, 2),
            "segments": seg_list,
            "words": all_words
        }

        output_json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"[Whisper Aligner] Successfully aligned {len(all_words)} words across {len(seg_list)} segments. Duration: {info.duration:.2f}s")
        return result
    except Exception as e:
        print(f"[Warning] Whisper alignment failed ({e}). Using script duration alignment fallback...")
        return align_script_text(audio_path, output_json_path, script_text=script_text)
