"""
Audio Mixer Module
Synthesizes atmospheric Lo-Fi ambient backing tracks and mixes audio
with automatic speech ducking.
"""

import math
import wave
import struct
import random
from pathlib import Path

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

def synthesize_lofi_track(duration: float, output_path: Path, sample_rate: int = 44100) -> Path:
    """
    Synthesizes a warm, soothing ambient lo-fi track with chord progressions
    and subtle vinyl crackle texture directly using pure Python or NumPy.
    """
    print(f"[Audio Mixer] Synthesizing {duration:.1f}s lo-fi ambient backing track...")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not HAS_NUMPY:
        # High-performance zero-dependency pure Python synthesizer
        total_samples = int(duration * sample_rate)
        buffer = [0.0] * total_samples
        chord_duration = 3.8
        num_chords = int(math.ceil(duration / chord_duration))
        chords = [
            [110.00, 130.81, 164.81, 196.00],  # Am7
            [87.31, 110.00, 130.81, 164.81],   # Fmaj7
            [130.81, 164.81, 196.00, 246.94],  # Cmaj7
            [98.00, 123.47, 146.83, 164.81]    # G6
        ]

        fade_len = int(0.25 * sample_rate)
        for i in range(num_chords):
            c = chords[i % len(chords)]
            start_s = int(i * chord_duration * sample_rate)
            end_s = min(int((i + 1) * chord_duration * sample_rate), total_samples)
            chunk_len = end_s - start_s
            if chunk_len <= 0:
                break
            for idx in range(chunk_len):
                t = idx / sample_rate
                # Envelope
                if idx < fade_len:
                    env = idx / fade_len
                elif idx > chunk_len - fade_len:
                    env = max(0.0, (chunk_len - idx) / fade_len)
                else:
                    env = 1.0
                val = 0.0
                for freq in c:
                    val += 0.35 * math.sin(2 * math.pi * freq * t)
                    val += 0.12 * math.sin(2 * math.pi * (freq * 2) * t)
                crackle = (random.random() - 0.5) * 0.012
                buffer[start_s + idx] += (val * env * 0.22) + crackle

        # Heartbeat kick
        beat_interval = 60.0 / 86.0
        t_kick = 0.0
        while t_kick < duration:
            ks = int(t_kick * sample_rate)
            klen = int(0.18 * sample_rate)
            for kidx in range(klen):
                if ks + kidx < total_samples:
                    kt = kidx / sample_rate
                    f = 60.0 - 30.0 * (kt / 0.18)
                    kick = math.sin(2 * math.pi * f * kt) * math.exp(-kt * 18) * 0.12
                    buffer[ks + kidx] += kick
            t_kick += beat_interval * 2

        # Write WAV directly using struct
        with wave.open(str(output_path), "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            frames = bytearray()
            for s in buffer:
                sample_val = int(max(-0.9, min(0.9, s)) * 32767)
                frame = struct.pack('<hh', sample_val, sample_val)
                frames.extend(frame)
            wf.writeframes(frames)
        print(f"[Audio Mixer] Lo-Fi track saved to {output_path}")
        return output_path

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
