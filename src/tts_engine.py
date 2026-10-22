"""
Voiceover / TTS Engine
Supports Deepgram Flagship Voice (Aura-2 Thalia) with smart chunking,
plus Edge-TTS fallback.
"""

import sys
import time
import asyncio
from pathlib import Path
from typing import Optional
import requests

from .config import DEEPGRAM_API_KEY, DEFAULT_DEEPGRAM_MODEL, DEFAULT_EDGE_VOICE

def synthesize_deepgram(
    text: str,
    output_path: Path,
    api_key: Optional[str] = None,
    model: str = DEFAULT_DEEPGRAM_MODEL
) -> Path:
    """
    Synthesizes voiceover via Deepgram TTS API with automatic chunking for long scripts.
    """
    key = api_key or DEEPGRAM_API_KEY
    if not key:
        raise ValueError("Deepgram API Key is required. Set DEEPGRAM_API_KEY in environment or .env file.")

    url = f"https://api.deepgram.com/v1/speak?model={model}"
    headers = {
        "Authorization": f"Token {key}",
        "Content-Type": "application/json"
    }

    # Chunk by paragraphs or short sentences (~400 characters) for reliable streaming
    chunks = []
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    for p in paragraphs:
        if len(p) <= 500:
            chunks.append(p)
        else:
            sentences = p.replace(". ", ".\n").splitlines()
            curr = []
            curr_len = 0
            for s in sentences:
                s = s.strip()
                if not s:
                    continue
                if curr_len + len(s) > 400:
                    chunks.append(" ".join(curr))
                    curr = [s]
                    curr_len = len(s)
                else:
                    curr.append(s)
                    curr_len += len(s) + 1
            if curr:
                chunks.append(" ".join(curr))

    print(f"[Deepgram TTS] Synthesizing with model '{model}' across {len(chunks)} chunk(s)...")
    combined_audio = bytearray()

    for idx, chunk in enumerate(chunks, 1):
        print(f"[Deepgram TTS] Chunk {idx}/{len(chunks)} ({len(chunk)} chars)...")
        last_err = None
        for attempt in range(3):
            try:
                r = requests.post(url, headers=headers, json={"text": chunk}, timeout=45)
                if r.status_code == 200:
                    combined_audio.extend(r.content)
                    last_err = None
                    break
                else:
                    last_err = RuntimeError(f"Deepgram API error {r.status_code}: {r.text}")
            except Exception as ex:
                last_err = ex
                time.sleep(1.5)
        if last_err:
            raise last_err

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(combined_audio)

    print(f"[Deepgram TTS] Successfully saved voiceover to {output_path} ({len(combined_audio)} bytes)")
    return output_path

async def _synthesize_edge_async(text: str, output_path: Path, voice: str):
    import edge_tts
    tts = edge_tts.Communicate(text, voice=voice, rate="+0%", pitch="+0Hz")
    await tts.save(str(output_path))

def synthesize_edge_tts(
    text: str,
    output_path: Path,
    voice: str = DEFAULT_EDGE_VOICE
) -> Path:
    """
    Synthesizes voiceover using Microsoft Edge Neural TTS (completely free fallback).
    """
    print(f"[Edge-TTS] Synthesizing voiceover with voice '{voice}'...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    asyncio.run(_synthesize_edge_async(text, output_path, voice))
    print(f"[Edge-TTS] Successfully saved voiceover to {output_path}")
    return output_path

def synthesize_windows_tts(
    text: str,
    output_path: Path,
    voice: str = "Mark"
) -> Path:
    """
    Synthesizes voiceover using native Windows SpeechSynthesizer (zero dependencies, completely offline).
    """
    import subprocess
    print(f"[Windows-TTS] Synthesizing voiceover with voice '{voice}'...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wav_path = output_path.with_suffix(".wav")
    temp_txt = output_path.with_suffix(".tmp.txt")
    temp_txt.write_text(text, encoding="utf-8")
    
    ps_cmd = f"""
    Add-Type -AssemblyName System.Speech;
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $voices = $synth.GetInstalledVoices() | ForEach-Object {{ $_.VoiceInfo.Name }};
    $sel = $voices | Where-Object {{ $_ -like '*{voice}*' }} | Select-Object -First 1;
    if (-not $sel) {{ $sel = $voices | Select-Object -First 1 }};
    if ($sel) {{ $synth.SelectVoice($sel) }};
    $synth.Rate = 0;
    $text = Get-Content -Path '{str(temp_txt.resolve())}' -Raw -Encoding UTF8;
    $synth.SetOutputToWaveFile('{str(wav_path.resolve())}');
    $synth.Speak($text);
    $synth.Dispose();
    """
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
    if temp_txt.exists():
        temp_txt.unlink()
    
    # If output_path requested was mp3, convert with ffmpeg, else return wav
    if output_path.suffix.lower() == ".mp3":
        from .config import FFMPEG_PATH
        subprocess.run([
            FFMPEG_PATH, "-y", "-i", str(wav_path.resolve()),
            "-codec:a", "libmp3lame", "-qscale:a", "2", str(output_path.resolve())
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if wav_path != output_path and wav_path.exists():
            wav_path.unlink()
    else:
        output_path = wav_path

    print(f"[Windows-TTS] Successfully saved voiceover to {output_path}")
    return output_path

def generate_voiceover(
    text: str,
    output_path: Path,
    provider: str = "deepgram",
    deepgram_key: Optional[str] = None
) -> Path:
    """
    Unified voiceover entrypoint with automatic provider selection and fallback.
    """
    if provider.lower() == "deepgram":
        try:
            return synthesize_deepgram(text, output_path, api_key=deepgram_key)
        except Exception as e:
            print(f"[Warning] Deepgram synthesis failed ({e}). Falling back to Edge/Windows TTS...")
            try:
                return synthesize_edge_tts(text, output_path)
            except Exception as e2:
                print(f"[Warning] Edge-TTS failed ({e2}). Falling back to native Windows TTS...")
                return synthesize_windows_tts(text, output_path)
    elif provider.lower() == "edge":
        try:
            return synthesize_edge_tts(text, output_path)
        except Exception as e:
            print(f"[Warning] Edge-TTS failed ({e}). Falling back to native Windows TTS...")
            return synthesize_windows_tts(text, output_path)
    else:
        return synthesize_windows_tts(text, output_path)
