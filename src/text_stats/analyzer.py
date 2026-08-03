"""Core text-analysis functionality."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import re


WORD_PATTERN = re.compile(r"[^\W\d_]+(?:['’\-][^\W\d_]+)*", re.UNICODE)
SENTENCE_SEPARATOR = re.compile(r"[.!?]+")


@dataclass(frozen=True, slots=True)
class TextStatistics:
    """Summary statistics for a piece of text."""

    characters: int
    characters_without_spaces: int
    words: int
    unique_words: int
    sentences: int
    lines: int
    top_words: tuple[tuple[str, int], ...]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation."""

        result = asdict(self)
        result["top_words"] = [
            {"word": word, "count": count} for word, count in self.top_words
        ]
        return result


def _count_sentences(text: str) -> int:
    return sum(bool(part.strip()) for part in SENTENCE_SEPARATOR.split(text))


def analyze_text(text: str, *, top_n: int = 5) -> TextStatistics:
    """Analyze *text* and return its most useful basic statistics.

    Args:
        text: Unicode text to analyze.
        top_n: Maximum number of frequent words to include.

    Raises:
        ValueError: If ``top_n`` is negative.
    """

    if top_n < 0:
        raise ValueError("top_n must be zero or greater")

    normalized_words = [match.group(0).casefold() for match in WORD_PATTERN.finditer(text)]
    frequencies = Counter(normalized_words)

    return TextStatistics(
        characters=len(text),
        characters_without_spaces=sum(not character.isspace() for character in text),
        words=len(normalized_words),
        unique_words=len(frequencies),
        sentences=_count_sentences(text),
        lines=len(text.splitlines()) if text else 0,
        top_words=tuple(frequencies.most_common(top_n)),
    )

