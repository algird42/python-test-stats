"""Command-line interface for the text analyzer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Sequence

from .analyzer import TextStatistics, analyze_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="text-stats",
        description="Calculate useful statistics for text.",
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("text", nargs="?", help="Text to analyze")
    source.add_argument("--file", type=Path, help="UTF-8 text file to analyze")
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        metavar="N",
        help="number of frequent words to show (default: 5)",
    )
    parser.add_argument("--json", action="store_true", help="print JSON output")
    return parser


def read_text(args: argparse.Namespace) -> str:
    if args.file is not None:
        return args.file.read_text(encoding="utf-8")
    if args.text is not None:
        return args.text
    if sys.stdin.isatty():
        raise ValueError("provide text, --file PATH, or pipe text through stdin")
    return sys.stdin.read()


def format_report(statistics: TextStatistics) -> str:
    lines = [
        f"Characters: {statistics.characters}",
        f"Characters without spaces: {statistics.characters_without_spaces}",
        f"Words: {statistics.words}",
        f"Unique words: {statistics.unique_words}",
        f"Sentences: {statistics.sentences}",
        f"Lines: {statistics.lines}",
        "Top words:",
    ]
    if statistics.top_words:
        lines.extend(f"  {word}: {count}" for word, count in statistics.top_words)
    else:
        lines.append("  (none)")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        text = read_text(args)
        statistics = analyze_text(text, top_n=args.top)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))

    if args.json:
        print(json.dumps(statistics.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(format_report(statistics))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

