"""
Video Renderer Module
Assembles image sequences, voiceover, ducked backing track, and burning karaoke
subtitles into a 9:16 vertical MP4 video using native FFmpeg.
"""

import subprocess
from pathlib import Path
from typing import List
from .config import FFMPEG_PATH, VIDEO_WIDTH, VIDEO_HEIGHT, FPS

def render_video(
    image_paths: List[Path],
    voiceover_path: Path,
    bgm_path: Path,
    subtitles_path: Path,
    duration: float,
    output_video_path: Path,
    bgm_volume: float = 0.15
) -> Path:
    """
    Renders high-retention 9:16 video.
    """
    num_images = len(image_paths)
    if num_images == 0:
        raise ValueError("Cannot render video with 0 images.")

    dur_per_img = duration / num_images
    print(f"[Video Renderer] Assembling {num_images} scenes ({dur_per_img:.2f}s per cut) for {duration:.2f}s total...")

    # Write concat list file
    concat_file = output_video_path.parent / "concat_scenes.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for img in image_paths:
            img_str = str(img.resolve()).replace("\\", "/")
            f.write(f"file '{img_str}'\n")
            f.write(f"duration {dur_per_img:.3f}\n")
        # Duplicate last frame for FFmpeg concat demuxer requirement
        last_str = str(image_paths[-1].resolve()).replace("\\", "/")
        f.write(f"file '{last_str}'\n")

    # Escape path for FFmpeg subtitles filter
    escaped_ass = str(subtitles_path.resolve()).replace("\\", "/").replace(":", "\\:")

    cmd = [
        FFMPEG_PATH, "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-i", str(voiceover_path.resolve()),
        "-i", str(bgm_path.resolve()),
        "-filter_complex",
        f"[0:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,"
        f"pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2:white,format=yuv420p,"
        f"subtitles='{escaped_ass}'[v];"
        f"[2:a]volume={bgm_volume}[bgm];[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-r", str(FPS),
        "-t", f"{duration:.2f}",
        str(output_video_path.resolve())
    ]

    log_path = output_video_path.parent / "ffmpeg_render.log"
    print(f"[Video Renderer] Encoding with FFmpeg (log: {log_path})...")
    with open(log_path, "w") as lf:
        res = subprocess.run(cmd, stdout=lf, stderr=lf)

    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg render failed with exit code {res.returncode}. See {log_path}")

    print(f"[Video Renderer] SUCCESS! Rendered video at: {output_video_path} ({output_video_path.stat().st_size / (1024*1024):.2f} MB)")
    return output_video_path
