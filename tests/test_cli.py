from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from bretontv import cli

SAMPLE_PLAYLIST = """#EXTM3U
#EXTINF:-1 tvg-country="CA" group-title="Ambiance",Spring Vibes
https://example.com/stream112.m3u8
#EXTINF:-1 tvg-country="US" group-title="News",US Breaking News
https://example.com/news.m3u8
"""


class CLITests(unittest.TestCase):
    def _write_playlist(self) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "playlist.m3u"
        path.write_text(SAMPLE_PLAYLIST, encoding="utf-8")
        return path

    def test_json_output_is_valid(self) -> None:
        playlist = self._write_playlist()
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = cli.main([str(playlist), "--format", "json", "--limit", "1"])
        self.assertEqual(exit_code, 0)
        payload = json.loads(buffer.getvalue())
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["group_title"], "Ambiance")

    def test_list_groups(self) -> None:
        playlist = self._write_playlist()
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = cli.main([str(playlist), "--list-groups"])
        self.assertEqual(exit_code, 0)
        output = buffer.getvalue().strip().splitlines()
        self.assertEqual(output, ["Ambiance", "News"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
