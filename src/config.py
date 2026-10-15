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

# FFmpeg tool discovery
FFMPEG_PATH = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE_PATH = shutil.which("ffprobe") or "ffprobe"

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
