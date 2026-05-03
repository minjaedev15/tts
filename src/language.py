# language.py
from functools import lru_cache
import langid

_LANG_CACHE_MAXSIZE = 128

@lru_cache(maxsize=_LANG_CACHE_MAXSIZE)
def _detect_language_cached(stripped_text: str) -> str:
    # stripped_text는 호출부에서 이미 trim 했다고 가정
    if len(stripped_text) < 3:
        return "en"
    lang, _ = langid.classify(stripped_text)
    return lang

def detect_language(text: str) -> str:
    stripped = text.strip()
    return _detect_language_cached(stripped)