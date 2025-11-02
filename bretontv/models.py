"""Data models used by the BretonTV playlist tooling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional


@dataclass(frozen=True)
class Channel:
    """Representation of a channel entry inside an M3U playlist."""

    name: str
    url: str
    tvg_chno: Optional[str] = None
    tvg_id: Optional[str] = None
    tvg_logo: Optional[str] = None
    tvg_country: Optional[str] = None
    group_title: Optional[str] = None

    def metadata(self) -> Mapping[str, Optional[str]]:
        """Return a mapping view of the metadata associated with the channel."""

        return {
            "tvg_chno": self.tvg_chno,
            "tvg_id": self.tvg_id,
            "tvg_logo": self.tvg_logo,
            "tvg_country": self.tvg_country,
            "group_title": self.group_title,
        }

    def matches(self, keyword: str) -> bool:
        """Return ``True`` if the channel matches the provided keyword."""

        lowered = keyword.casefold()
        candidates = [self.name, self.url, self.tvg_id, self.group_title]
        return any(value and lowered in value.casefold() for value in candidates)
