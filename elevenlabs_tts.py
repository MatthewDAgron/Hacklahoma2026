import os
import subprocess
import sys


def play_audio(sound_file):
    """Play an audio file (MP3). Non-blocking. Uses ffplay (auto-closes); falls back to os.startfile on Windows."""
    if not os.path.exists(sound_file):
        return
    try:
        # ffplay with -autoexit closes when done; works on Windows if ffmpeg is installed
        subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", sound_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        if sys.platform == "win32":
            os.startfile(sound_file)  # Opens default player (may stay open)


def main():
    play_audio("sounds/mickey.mp3")


if __name__ == "__main__":
    main()
