"""Filtering and sorting utilities for channel collections."""

from __future__ import annotations

from typing import Iterable, List, Optional, Sequence

from .models import Channel


def filter_channels(
    channels: Sequence[Channel],
    *,
    country: Optional[str] = None,
    group: Optional[str] = None,
    keyword: Optional[str] = None,
) -> List[Channel]:
    """Return the subset of *channels* that matches the provided criteria."""

    filtered: Iterable[Channel] = channels
    if country:
        lowered = country.casefold()
        filtered = [
            channel
            for channel in filtered
            if channel.tvg_country and channel.tvg_country.casefold() == lowered
        ]
    if group:
        lowered = group.casefold()
        filtered = [
            channel
            for channel in filtered
            if channel.group_title and channel.group_title.casefold() == lowered
        ]
    if keyword:
        filtered = [channel for channel in filtered if channel.matches(keyword)]
    return list(filtered)


def sort_channels(channels: Sequence[Channel]) -> List[Channel]:
    """Return *channels* sorted by channel number, group, and name."""

    def sort_key(channel: Channel) -> tuple:
        def parse_channel_number(value: Optional[str]) -> tuple[int, str]:
            if value is None:
                return (1, "")
            try:
                return (0, f"{int(value):04d}")
            except ValueError:
                return (1, value)

        return (
            parse_channel_number(channel.tvg_chno),
            (channel.group_title or "").casefold(),
            channel.name.casefold(),
        )

    return sorted(channels, key=sort_key)
