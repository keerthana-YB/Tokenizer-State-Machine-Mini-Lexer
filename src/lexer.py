"""
Group 3: Tokenizer State Machine (Mini Lexer)
Member 2: Lexer Implementation - Stage 1

This module defines the Token data model and the Lexer foundation.
"""

from dataclasses import dataclass
from typing import List, Optional
from src.dfa import (
    State,
    CharacterClass,
    transition,
    is_accepting,
    get_token_type,
    classify_character,
)


@dataclass
class Token:
    """
    Represents a lexical token emitted by the DFA lexer.

    Attributes:
        lexeme: The substring matched from the input text.
        type: The token category (IDENTIFIER, NUMBER, WHITESPACE, PUNCTUATION, UNKNOWN).
        start: Starting character index in the source text (0-indexed, inclusive).
        end: Ending character index in the source text (0-indexed, exclusive).
    """
    lexeme: str
    type: str
    start: int
    end: int

    def __repr__(self) -> str:
        return f"({self.lexeme!r}, {self.type}) at position {self.start}-{self.end}"


class Lexer:
    """
    DFA-driven lexical analyzer (tokenizer) that splits raw character streams
    into structured Token instances based on formal state transitions.
    """

    def __init__(self) -> None:
        pass
