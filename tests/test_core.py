import os
import tempfile
import unittest

import src.core as core


class TestCore(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["TTS_DISABLE_TTS"] = "1"
        os.environ["TTS_DISABLE_AUDIO"] = "1"

    def tearDown(self) -> None:
        os.environ.pop("TTS_DISABLE_TTS", None)
        os.environ.pop("TTS_DISABLE_AUDIO", None)

    def test_speak_returns_mp3_path_and_creates_file(self) -> None:
        text = "안녕하세요 CI 테스트"
        mp3_path = core.speak(text)

        self.assertIsInstance(mp3_path, str)
        self.assertTrue(mp3_path.endswith(".mp3"))
        self.assertTrue(os.path.exists(mp3_path), "speak() should create a placeholder mp3 when TTS is disabled")

        # Placeholder file content may be tiny; just ensure non-zero size (or at least readable).
        self.assertGreaterEqual(os.path.getsize(mp3_path), 3)

        # Cleanup best-effort.
        try:
            os.remove(mp3_path)
        except OSError:
            pass


if __name__ == "__main__":
    unittest.main()
