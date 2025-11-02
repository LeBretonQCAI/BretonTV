from __future__ import annotations

import unittest

from bretontv.models import Channel
from bretontv.parser import PlaylistFormatError, parse_text


SAMPLE_PLAYLIST = """#EXTM3U
#EXTINF:-1 tvg-chno="112" tvg-id="CA14000121V" tvg-logo="https://example.com/logo112.png" tvg-country="CA" group-title="Ambiance",112. Spring Vibes
https://example.com/stream112.m3u8
#EXTINF:-1 tvg-id="USNEWS" tvg-country="US" group-title="News",US Breaking News
https://example.com/news.m3u8
"""


class ParserTests(unittest.TestCase):
    def test_parse_text_returns_channels(self) -> None:
        channels = parse_text(SAMPLE_PLAYLIST)
        self.assertEqual(len(channels), 2)

        first = channels[0]
        self.assertIsInstance(first, Channel)
        self.assertEqual(first.name, "112. Spring Vibes")
        self.assertEqual(first.url, "https://example.com/stream112.m3u8")
        self.assertEqual(first.tvg_chno, "112")
        self.assertEqual(first.group_title, "Ambiance")

        second = channels[1]
        self.assertEqual(second.tvg_country, "US")
        self.assertEqual(second.group_title, "News")

    def test_missing_url_raises_error(self) -> None:
        malformed = "#EXTM3U\n#EXTINF:-1 tvg-id=\"MISSING\",Test Channel\n"
        with self.assertRaises(PlaylistFormatError):
            parse_text(malformed)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
