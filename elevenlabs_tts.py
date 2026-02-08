import subprocess


def play_audio(sound_file):
    """Play an audio file (e.g. MP3). Uses ffplay (ffmpeg) - no Python audio deps. Works on AWS/Linux."""
    try:
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", sound_file],
            check=True,
            timeout=120,
            capture_output=True,
        )
    except FileNotFoundError:
        pass  # ffplay not installed (install ffmpeg), skip playback
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        pass


def main():
    play_audio("sounds/ElevenLabs_2026-02-08T03_10_28_Northern Terry_pvc_sp87_s30_sb90_se38_b_m2.mp3")


if __name__ == "__main__":
    main()
