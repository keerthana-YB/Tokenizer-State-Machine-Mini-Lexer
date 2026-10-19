
"""
Group 3: Tokenizer State Machine (Mini Lexer)
Member 4: Mini Lexer vs GPT Tokenizer Comparison
"""

from dataclasses import dataclass

import tiktoken
from src.lexer import tokenize


@dataclass
class TokenCountComparison:
    """Stores token counts from both tokenizers."""

    lexer_token_count: int
    gpt_token_count: int

    @property
    def difference(self) -> int:
        """GPT token count minus mini-lexer token count."""
        return self.gpt_token_count - self.lexer_token_count


def compare_token_counts(
    text: str,
    encoding_name: str = "cl100k_base",
) -> TokenCountComparison:
    """Compare the mini-lexer count with a GPT-compatible tokenizer."""

    lexer_tokens = tokenize(text)

    encoding = tiktoken.get_encoding(encoding_name)
    gpt_tokens = encoding.encode(text, disallowed_special=())

    return TokenCountComparison(
        lexer_token_count=len(lexer_tokens),
        gpt_token_count=len(gpt_tokens),
    )
