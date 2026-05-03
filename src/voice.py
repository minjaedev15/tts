# voice.py
import asyncio
import threading
from collections import OrderedDict
import edge_tts

# 🔁 Cache voices to avoid repeated network calls to edge_tts.list_voices()
_VOICE_CACHE: list[dict[str, str]] | None = None
_VOICE_CACHE_LOCK = threading.Lock()

# Additional caches for performance (CPU/dict work)
_VOICE_BY_LANG_CACHE_MAXSIZE = 128
_VOICE_BY_LANG_CACHE_LOCK = threading.Lock()
_VOICE_BY_LANG_CACHE: OrderedDict[str, str] = OrderedDict()

async def load_voices() -> list[dict[str, str]]:
    global _VOICE_CACHE
    if _VOICE_CACHE is None:
        # edge_tts.list_voices() is async, but cache state is shared across threads.
        with _VOICE_CACHE_LOCK:
            if _VOICE_CACHE is None:
                _VOICE_CACHE = await edge_tts.list_voices()
    return _VOICE_CACHE

async def pick_voice(lang: str) -> str:
    # Fast-path: cached voice lookup (real LRU via OrderedDict).
    normalized = (lang or "").strip()
    with _VOICE_BY_LANG_CACHE_LOCK:
        cached = _VOICE_BY_LANG_CACHE.get(normalized)
        if cached is not None:
            _VOICE_BY_LANG_CACHE.move_to_end(normalized)
            return cached

    voices = await load_voices()
    lang_prefix = (lang or "").lower()

    picked = "en-US-AriaNeural"
    for v in voices:
        locale = (v.get("Locale") or "").lower()
        if locale.startswith(lang_prefix):
            picked = v.get("ShortName") or "en-US-AriaNeural"
            break

    with _VOICE_BY_LANG_CACHE_LOCK:
        # Insert/update and evict LRU
        if normalized in _VOICE_BY_LANG_CACHE:
            _VOICE_BY_LANG_CACHE.move_to_end(normalized)
        _VOICE_BY_LANG_CACHE[normalized] = picked
        while len(_VOICE_BY_LANG_CACHE) > _VOICE_BY_LANG_CACHE_MAXSIZE:
            _VOICE_BY_LANG_CACHE.popitem(last=False)

    return picked