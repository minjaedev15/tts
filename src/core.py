# core.py
from __future__ import annotations

import asyncio
import os
import tempfile
import threading

import edge_tts

from .language import detect_language
from .voice import pick_voice
from .audio import play_audio

_TMP_CLEANUP_DEFAULT_SECONDS = 30.0


def _env_flag(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _should_disable_audio() -> bool:
    return _env_flag("TTS_DISABLE_AUDIO")


def _should_disable_tts() -> bool:
    return _env_flag("TTS_DISABLE_TTS")


def _should_disable_cleanup() -> bool:
    return _env_flag("TTS_DISABLE_CLEANUP")


def _cleanup_seconds() -> float:
    raw = os.getenv("TTS_TEMP_CLEANUP_SECONDS", "").strip()
    if not raw:
        return _TMP_CLEANUP_DEFAULT_SECONDS
    try:
        return float(raw)
    except ValueError:
        return _TMP_CLEANUP_DEFAULT_SECONDS


def _schedule_cleanup(path: str) -> None:
    if _should_disable_cleanup():
        return

    delay = _cleanup_seconds()
    if delay <= 0:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            pass
        return

    def _delete_if_exists() -> None:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            pass

    t = threading.Timer(delay, _delete_if_exists)
    t.daemon = True
    t.start()





def _create_placeholder_mp3(tmp_path: str) -> None:
    # Best-effort placeholder so CI/workflows can validate file creation.
    # Note: this is not a fully valid MP3; it should only be used when audio/TTS are disabled.
    try:
        with open(tmp_path, "wb") as f:
            f.write(b"ID3")
    except OSError:
        pass


async def tts_make(text: str) -> str:
    # Create a unique temp path per request to avoid races/stale globals.
    fd, tmp_path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)

    if _should_disable_tts():
        _create_placeholder_mp3(tmp_path)

        # Even if audio is disabled, schedule cleanup to avoid temp accumulation.
        _schedule_cleanup(tmp_path)

        if _should_disable_audio():
            return tmp_path

        play_audio(tmp_path)
        return tmp_path

    lang = detect_language(text)
    voice = await pick_voice(lang)

    await edge_tts.Communicate(text, voice).save(tmp_path)

    # If audio disabled, don't play—but still schedule cleanup for performance/space.
    if _should_disable_audio():
        _schedule_cleanup(tmp_path)
        return tmp_path

    # Play and schedule cleanup.
    _schedule_cleanup(tmp_path)
    play_audio(tmp_path)
    return tmp_path


def speak(text: str) -> str:
    """
    Synchronous API called from the UI thread.

    Returns the generated/placeholder mp3 path.
    Temp files are automatically cleaned up unless TTS_DISABLE_CLEANUP is set.
    """
    return asyncio.run(tts_make(text))


if __name__ == "__main__":
    # Minimal manual test.
    print(speak("테스트입니다. CI에서는 TTS_DISABLE_AUDIO=1로 실행하세요."))
