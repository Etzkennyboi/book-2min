import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = BASE_DIR / "templates"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

# Deepgram settings
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")
DEFAULT_DEEPGRAM_MODEL = os.getenv("DEEPGRAM_VOICE_MODEL", "aura-2-thalia-en")

# Edge-TTS fallback
DEFAULT_EDGE_VOICE = os.getenv("EDGE_TTS_VOICE", "en-US-ChristopherNeural")

# Video render settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30
ASPECT_RATIO = "9:16"

# Fast GPU Rendering Pipeline configuration
GPU_ACCEL_ENABLED = True
GPU_ENCODER = "h264_qsv"           # Intel Quick Sync Video hardware acceleration
GPU_PRESET = "veryfast"
FALLBACK_ENCODER = "libx264"

# FFmpeg tool discovery
def _find_ffmpeg():
    found = shutil.which("ffmpeg")
    if found:
        return found
    winget_cand = list(Path.home().glob("AppData/Local/Microsoft/WinGet/Packages/*FFmpeg*/**/ffmpeg.exe"))
    if winget_cand:
        return str(winget_cand[0])
    return "ffmpeg"

def _find_ffprobe():
    found = shutil.which("ffprobe")
    if found:
        return found
    winget_cand = list(Path.home().glob("AppData/Local/Microsoft/WinGet/Packages/*FFmpeg*/**/ffprobe.exe"))
    if winget_cand:
        return str(winget_cand[0])
    return "ffprobe"

FFMPEG_PATH = _find_ffmpeg()
FFPROBE_PATH = _find_ffprobe()

# Subtitle styling (StickLit high-retention karaoke specification)
SUBTITLE_STYLE = {
    "font_name": "Arial",
    "font_size": 56,
    "primary_color": "&H00FFFFFF",     # Pure White
    "active_color": "&H0000E6FF",      # Vibrant Golden Yellow (\c&H0000E6FF&)
    "outline_color": "&H00000000",     # Solid Black Outline
    "back_color": "&H80000000",        # Subtle translucent shadow
    "outline_width": 5.5,
    "shadow_depth": 2.0,
    "alignment": 2,                    # Bottom-center
    "margin_v": 280                    # Lower-middle third
}
