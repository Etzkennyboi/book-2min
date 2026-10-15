"""
Speech Aligner Module
Extracts millisecond-accurate word-level and segment-level timestamps
using faster-whisper.
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
from faster_whisper import WhisperModel

def load_audio_ffmpeg(file_path: Path) -> np.ndarray:
    """
    Decodes audio to 16kHz mono float32 numpy array using FFmpeg subprocess
    to avoid libav C-extension version issues.
    """
    cmd = [
        "ffmpeg", "-nostdin", "-threads", "0", "-i", str(file_path),
        "-f", "s16le", "-ac", "1", "-acodec", "pcm_s16le", "-ar", "16000", "-"
    ]
    out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

def align_speech(
    audio_path: Path,
    output_json_path: Path,
    model_size: str = "base.en"
) -> Dict[str, Any]:
    """
    Transcribes audio and extracts word timestamps.
    """
    print(f"[Whisper Aligner] Loading Whisper {model_size} model...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print(f"[Whisper Aligner] Aligning audio words from {audio_path}...")
    audio_data = load_audio_ffmpeg(audio_path)
    segments, info = model.transcribe(audio_data, beam_size=5, word_timestamps=True)

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
