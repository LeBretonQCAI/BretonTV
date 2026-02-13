from __future__ import annotations

import unittest

from bretontv.filters import filter_channels, sort_channels
from bretontv.models import Channel


class FilterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.channels = [
            Channel(name="A", url="http://example.com/a", tvg_country="CA", group_title="News", tvg_chno="10"),
            Channel(name="B", url="http://example.com/b", tvg_country="US", group_title="Sports", tvg_chno="2"),
            Channel(name="C", url="http://example.com/c", tvg_country="CA", group_title="News"),
        ]

    def test_filter_by_country(self) -> None:
        filtered = filter_channels(self.channels, country="ca")
        self.assertEqual({channel.name for channel in filtered}, {"A", "C"})

    def test_filter_by_group(self) -> None:
        filtered = filter_channels(self.channels, group="sports")
        self.assertEqual([channel.name for channel in filtered], ["B"])

    def test_filter_by_keyword(self) -> None:
        filtered = filter_channels(self.channels, keyword="example.com/b")
        self.assertEqual([channel.name for channel in filtered], ["B"])

    def test_sort_channels(self) -> None:
        sorted_channels = sort_channels(self.channels)
        self.assertEqual([channel.name for channel in sorted_channels], ["B", "A", "C"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
