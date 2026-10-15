"""
Audio Mixer Module
Synthesizes atmospheric Lo-Fi ambient backing tracks and mixes audio
with automatic speech ducking.
"""

import math
import wave
from pathlib import Path
import numpy as np

def synthesize_lofi_track(duration: float, output_path: Path, sample_rate: int = 44100) -> Path:
    """
    Synthesizes a warm, soothing ambient lo-fi track with chord progressions
    and subtle vinyl crackle texture directly using pure NumPy/wave.
    """
    print(f"[Audio Mixer] Synthesizing {duration:.1f}s lo-fi ambient backing track...")
    total_samples = int(duration * sample_rate)
    audio_synth = np.zeros(total_samples, dtype=np.float32)

    chord_duration = 3.8
    num_chords = int(math.ceil(duration / chord_duration))
    chords = [
        [110.00, 130.81, 164.81, 196.00],  # Am7
        [87.31, 110.00, 130.81, 164.81],   # Fmaj7
        [130.81, 164.81, 196.00, 246.94],  # Cmaj7
        [98.00, 123.47, 146.83, 164.81]    # G6
    ]

    for i in range(num_chords):
        c = chords[i % len(chords)]
        start_s = int(i * chord_duration * sample_rate)
        end_s = min(int((i + 1) * chord_duration * sample_rate), total_samples)
        length = end_s - start_s
        if length <= 0:
            break
        t_chunk = np.linspace(0, length / sample_rate, length, endpoint=False)
        
        # Soft envelope
        env = np.ones(length, dtype=np.float32)
        fade_len = int(0.25 * sample_rate)
        if length > 2 * fade_len:
            env[:fade_len] = np.linspace(0, 1, fade_len)
            env[-fade_len:] = np.linspace(1, 0, fade_len)

        chunk_wave = np.zeros(length, dtype=np.float32)
        for freq in c:
            chunk_wave += 0.35 * np.sin(2 * np.pi * freq * t_chunk)
            chunk_wave += 0.12 * np.sin(2 * np.pi * (freq * 2) * t_chunk)

        # Subtle vinyl crackle
        noise = np.random.normal(0, 0.006, length).astype(np.float32)
        audio_synth[start_s:end_s] += (chunk_wave * env * 0.22) + noise

    # Subtle heartbeat kick on beats
    beat_interval = 60.0 / 86.0
    for kt in np.arange(0, duration, beat_interval * 2):
        ks = int(kt * sample_rate)
        klen = int(0.18 * sample_rate)
        if ks + klen < total_samples:
            kt_arr = np.linspace(0, 0.18, klen, endpoint=False)
            kick = np.sin(2 * np.pi * (60 - 30 * (kt_arr / 0.18)) * kt_arr) * np.exp(-kt_arr * 18) * 0.12
            audio_synth[ks:ks + klen] += kick

    # Normalize to 16-bit stereo PCM
    audio_int16 = (np.clip(audio_synth, -0.9, 0.9) * 32767).astype(np.int16)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        stereo = np.column_stack((audio_int16, audio_int16)).flatten()
        wf.writeframes(stereo.tobytes())

    print(f"[Audio Mixer] Lo-Fi track saved to {output_path}")
    return output_path
