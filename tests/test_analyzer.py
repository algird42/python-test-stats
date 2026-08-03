"""Tests for the public text-analysis API."""

import unittest

from text_stats import analyze_text


class AnalyzeTextTests(unittest.TestCase):
    def test_empty_text(self) -> None:
        statistics = analyze_text("")

        self.assertEqual(statistics.characters, 0)
        self.assertEqual(statistics.words, 0)
        self.assertEqual(statistics.sentences, 0)
        self.assertEqual(statistics.lines, 0)
        self.assertEqual(statistics.top_words, ())

    def test_counts_words_sentences_and_lines(self) -> None:
        statistics = analyze_text("Hello world!\nPython works.")

        self.assertEqual(statistics.words, 4)
        self.assertEqual(statistics.unique_words, 4)
        self.assertEqual(statistics.sentences, 2)
        self.assertEqual(statistics.lines, 2)

    def test_word_frequency_is_case_insensitive(self) -> None:
        statistics = analyze_text("Python python PYTHON code", top_n=2)

        self.assertEqual(statistics.top_words, (("python", 3), ("code", 1)))

    def test_unicode_words_and_hyphenation(self) -> None:
        statistics = analyze_text("Привет, мир! Привет — test-driven.")

        self.assertEqual(statistics.words, 4)
        self.assertEqual(statistics.unique_words, 3)
        self.assertEqual(statistics.top_words[0], ("привет", 2))

    def test_rejects_negative_top_limit(self) -> None:
        with self.assertRaisesRegex(ValueError, "top_n"):
            analyze_text("example", top_n=-1)


if __name__ == "__main__":
    unittest.main()

