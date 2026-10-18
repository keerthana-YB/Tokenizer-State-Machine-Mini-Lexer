"""
Group 3: Tokenizer State Machine (Mini Lexer)
Unit Tests for Member 2 Lexer Implementation
"""

import unittest
from src.lexer import Token, tokenize, Lexer


class TestDFALexer(unittest.TestCase):
    """Test suite verifying DFA-based lexical scanning and token generation."""

    def setUp(self) -> None:
        self.lexer = Lexer()

    def test_empty_string(self) -> None:
        """Empty input should yield an empty list of tokens."""
        self.assertEqual(tokenize(""), [])

    def test_single_identifier(self) -> None:
        """Single word should emit one IDENTIFIER token."""
        tokens = tokenize("hello")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0], Token("hello", "IDENTIFIER", 0, 5))

    def test_single_number(self) -> None:
        """Digits should emit one NUMBER token."""
        tokens = tokenize("12345")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0], Token("12345", "NUMBER", 0, 5))

    def test_single_punctuation(self) -> None:
        """Punctuation mark should emit one PUNCTUATION token."""
        tokens = tokenize("!")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0], Token("!", "PUNCTUATION", 0, 1))

    def test_whitespace_grouping(self) -> None:
        """Consecutive whitespace characters should be grouped into a single token."""
        text = "   \t\n  "
        tokens = tokenize(text)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0], Token(text, "WHITESPACE", 0, len(text)))

    def test_project_sample_sentence(self) -> None:
        """Verify the exact project sample sentence: 'Hello world! 42 tokens.'"""
        text = "Hello world! 42 tokens."
        tokens = tokenize(text)
        expected = [
            Token("Hello", "IDENTIFIER", 0, 5),
            Token(" ", "WHITESPACE", 5, 6),
            Token("world", "IDENTIFIER", 6, 11),
            Token("!", "PUNCTUATION", 11, 12),
            Token(" ", "WHITESPACE", 12, 13),
            Token("42", "NUMBER", 13, 15),
            Token(" ", "WHITESPACE", 15, 16),
            Token("tokens", "IDENTIFIER", 16, 22),
            Token(".", "PUNCTUATION", 22, 23),
        ]
        self.assertEqual(tokens, expected)

    def test_code_expression(self) -> None:
        """Verify assignment statement: 'count = 123;'"""
        text = "count = 123;"
        tokens = tokenize(text)
        expected = [
            Token("count", "IDENTIFIER", 0, 5),
            Token(" ", "WHITESPACE", 5, 6),
            Token("=", "PUNCTUATION", 6, 7),
            Token(" ", "WHITESPACE", 7, 8),
            Token("123", "NUMBER", 8, 11),
            Token(";", "PUNCTUATION", 11, 12),
        ]
        self.assertEqual(tokens, expected)

    def test_alphanumeric_and_number_prefix(self) -> None:
        """Identifiers can contain digits (count42), but numbers cannot contain letters (42tokens -> 42, tokens)."""
        tokens_id = tokenize("count42")
        self.assertEqual(len(tokens_id), 1)
        self.assertEqual(tokens_id[0], Token("count42", "IDENTIFIER", 0, 7))

        tokens_num = tokenize("42tokens")
        self.assertEqual(len(tokens_num), 2)
        self.assertEqual(tokens_num[0], Token("42", "NUMBER", 0, 2))
        self.assertEqual(tokens_num[1], Token("tokens", "IDENTIFIER", 2, 8))

    def test_consecutive_punctuation(self) -> None:
        """Each punctuation character is emitted individually by definition."""
        tokens = tokenize("?!;")
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0], Token("?", "PUNCTUATION", 0, 1))
        self.assertEqual(tokens[1], Token("!", "PUNCTUATION", 1, 2))
        self.assertEqual(tokens[2], Token(";", "PUNCTUATION", 2, 3))

    def test_unsupported_characters(self) -> None:
        """Characters outside character classes are emitted as UNKNOWN tokens without crashing."""
        text = "A © B"
        tokens = tokenize(text)
        self.assertEqual(tokens[0], Token("A", "IDENTIFIER", 0, 1))
        self.assertEqual(tokens[1], Token(" ", "WHITESPACE", 1, 2))
        self.assertEqual(tokens[2], Token("©", "UNKNOWN", 2, 3))
        self.assertEqual(tokens[3], Token(" ", "WHITESPACE", 3, 4))
        self.assertEqual(tokens[4], Token("B", "IDENTIFIER", 4, 5))

    def test_span_integrity(self) -> None:
        """Verify that slicing text[start:end] always equals the token lexeme for all tokens."""
        sample_texts = [
            "Hello world! 42 tokens.",
            "def foo(x, y=10): return x + y * 2",
            "   padded \t text with 999 items   ",
        ]
        for text in sample_texts:
            tokens = tokenize(text)
            for tok in tokens:
                self.assertEqual(text[tok.start:tok.end], tok.lexeme)


if __name__ == "__main__":
    unittest.main()
