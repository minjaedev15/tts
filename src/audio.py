# audio.py
import os
import platform
import subprocess
import threading

def play_audio(path: str) -> None:
    system = platform.system()

    # Keep playback non-blocking across platforms (performance / thread friendliness).
    if system == "Darwin":
        subprocess.Popen(
            ["afplay", path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return

    if system == "Windows":
        # os.startfile is non-blocking.
        os.startfile(path)  # type: ignore[attr-defined]
        return

    # Linux/other: non-blocking. xdg-open returns immediately.
    subprocess.Popen(
        ["xdg-open", path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )