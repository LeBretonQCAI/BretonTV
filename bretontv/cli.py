"""Command-line interface for exploring BretonTV playlists."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable, Sequence

from .filters import filter_channels, sort_channels
from .parser import load_channels


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bretontv",
        description="Explore and filter BretonTV M3U playlists.",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="One or more .m3u files or directories containing playlists.",
    )
    parser.add_argument(
        "--country",
        help="Filter channels by ISO country code (case insensitive).",
    )
    parser.add_argument(
        "--group",
        help="Filter channels by their group-title metadata.",
    )
    parser.add_argument(
        "--search",
        help="Return only channels matching the given keyword.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit the number of channels displayed.",
    )
    parser.add_argument(
        "--format",
        choices=("table", "json"),
        default="table",
        help="Output format for the results.",
    )
    parser.add_argument(
        "--list-groups",
        action="store_true",
        help="Show the available groups and exit.",
    )
    parser.add_argument(
        "--list-countries",
        action="store_true",
        help="Show the available countries and exit.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    try:
        channels = load_channels(args.paths)
    except FileNotFoundError as exc:
        parser.error(f"Unable to locate {exc}")

    channels = sort_channels(
        filter_channels(
            channels,
            country=args.country,
            group=args.group,
            keyword=args.search,
        )
    )

    if args.list_groups:
        _print_unique((channel.group_title for channel in channels if channel.group_title))
        return 0
    if args.list_countries:
        _print_unique((channel.tvg_country for channel in channels if channel.tvg_country))
        return 0

    if args.limit is not None:
        channels = channels[: args.limit]

    if args.format == "json":
        json.dump([_channel_to_dict(channel) for channel in channels], sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        _print_table(channels)
    return 0


def _channel_to_dict(channel) -> dict:
    data = channel.metadata() | {"name": channel.name, "url": channel.url}
    return {key: value for key, value in data.items() if value is not None}


def _print_unique(values: Iterable[str]) -> None:
    seen = set()
    for value in values:
        if value not in seen:
            print(value)
            seen.add(value)


def _print_table(channels) -> None:
    if not channels:
        print("No channels matched the provided criteria.")
        return

    headers = ["Name", "Country", "Group", "URL"]
    rows = [
        [
            channel.name,
            channel.tvg_country or "-",
            channel.group_title or "-",
            _shorten(channel.url, 70),
        ]
        for channel in channels
    ]

    column_widths = [
        max(len(header), *(len(row[idx]) for row in rows))
        for idx, header in enumerate(headers)
    ]

    _print_row(headers, column_widths)
    _print_row(["=" * width for width in column_widths], column_widths)
    for row in rows:
        _print_row(row, column_widths)


def _print_row(values, widths) -> None:
    print("  ".join(value.ljust(width) for value, width in zip(values, widths)))


def _shorten(text: str, max_length: int) -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())
