"""
Voiceover / TTS Engine
Supports Deepgram Flagship Voice (Aura-2 Thalia) with smart chunking,
plus Edge-TTS fallback.
"""

import sys
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

    # Deepgram limits text payloads to 2000 characters. We chunk by sentences/paragraphs.
    chunks = []
    current_chunk = []
    current_len = 0

    sentences = text.replace(". ", ".\n").splitlines()
    for sentence in sentences:
        s = sentence.strip()
        if not s:
            continue
        if current_len + len(s) + 1 > 1800:
            chunks.append(" ".join(current_chunk))
            current_chunk = [s]
            current_len = len(s)
        else:
            current_chunk.append(s)
            current_len += len(s) + 1

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    print(f"[Deepgram TTS] Synthesizing with model '{model}' across {len(chunks)} chunk(s)...")
    combined_audio = bytearray()

    for idx, chunk in enumerate(chunks, 1):
        r = requests.post(url, headers=headers, json={"text": chunk})
        if r.status_code != 200:
            raise RuntimeError(f"Deepgram API error {r.status_code} on chunk {idx}: {r.text}")
        combined_audio.extend(r.content)

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
            print(f"[Warning] Deepgram synthesis failed ({e}). Falling back to Edge-TTS...")
            return synthesize_edge_tts(text, output_path)
    else:
        return synthesize_edge_tts(text, output_path)
