"""M3U playlist parsing utilities for BretonTV."""

from __future__ import annotations

import pathlib
import re
from typing import Iterable, Iterator, List, Sequence

from .models import Channel

_EXTINF_PATTERN = re.compile(r"([A-Za-z0-9-]+)=\"([^\"]*)\"")


class PlaylistFormatError(ValueError):
    """Raised when a playlist entry is malformed."""


def parse_text(text: str) -> List[Channel]:
    """Parse an M3U playlist from a string."""

    return list(_iter_channels(text.splitlines()))


def parse_file(path: pathlib.Path | str) -> List[Channel]:
    """Parse an M3U playlist file."""

    file_path = pathlib.Path(path)
    with file_path.open("r", encoding="utf-8", errors="replace") as handle:
        return list(_iter_channels(handle))


def load_channels(paths: Sequence[pathlib.Path | str]) -> List[Channel]:
    """Load channels from the provided M3U files or directories."""

    collected: List[Channel] = []
    for raw_path in paths:
        path = pathlib.Path(raw_path)
        if path.is_dir():
            for child in sorted(path.rglob("*.m3u")):
                collected.extend(parse_file(child))
        elif path.is_file():
            collected.extend(parse_file(path))
        else:
            raise FileNotFoundError(path)
    return collected


def _iter_channels(lines: Iterable[str]) -> Iterator[Channel]:
    iterator = iter(lines)
    for line in iterator:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#EXTM3U"):
            continue
        if stripped.startswith("#EXTINF"):
            metadata, name = _split_metadata(stripped)
            attributes = dict(_EXTINF_PATTERN.findall(metadata))
            url = _consume_stream_url(iterator)
            yield Channel(
                name=name,
                url=url,
                tvg_chno=attributes.get("tvg-chno"),
                tvg_id=attributes.get("tvg-id"),
                tvg_logo=attributes.get("tvg-logo"),
                tvg_country=attributes.get("tvg-country"),
                group_title=attributes.get("group-title"),
            )
        elif stripped.startswith("#"):
            # Ignore other comment directives.
            continue
        else:
            raise PlaylistFormatError(f"Unexpected line outside an entry: {stripped!r}")


def _split_metadata(header: str) -> tuple[str, str]:
    if "," not in header:
        raise PlaylistFormatError(f"Entry is missing the channel name: {header!r}")
    metadata, name = header.split(",", 1)
    name = name.strip()
    if not name:
        raise PlaylistFormatError(f"Entry is missing the channel name: {header!r}")
    return metadata, name


def _consume_stream_url(iterator: Iterator[str]) -> str:
    for line in iterator:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            # Skip directives that occasionally appear between the metadata and the URL.
            continue
        return stripped
    raise PlaylistFormatError("Missing stream URL for channel entry")
