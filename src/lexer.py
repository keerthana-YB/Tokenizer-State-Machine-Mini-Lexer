"""
Group 3: Tokenizer State Machine (Mini Lexer)
Member 2: Lexer Implementation

This module implements character-by-character lexical scanning using the
Deterministic Finite Automaton (DFA) defined in src.dfa.
It follows the Maximal Munch (longest match) principle to emit tokens
with their lexeme, token type, and character span offsets.
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

    def tokenize(self, text: str) -> List[Token]:
        """
        Scan and tokenize the input string character-by-character using the DFA.

        Applies the Maximal Munch principle: consumes characters as long as valid
        transitions exist. When a transition leads to State.DEAD or end-of-input,
        the accumulated characters up to the last accepting state are emitted as a token.

        Args:
            text: Input string to tokenize.

        Returns:
            List of Token instances preserving character offsets.
        """
        tokens: List[Token] = []
        n = len(text)
        cursor = 0

        while cursor < n:
            start_pos = cursor
            current_state = State.START
            last_accepting_state: Optional[State] = None
            last_accepting_idx = -1

            scan_idx = cursor
            while scan_idx < n:
                char = text[scan_idx]
                next_state = transition(current_state, char)

                if next_state == State.DEAD:
                    # Token boundary reached: cannot continue current pattern
                    break

                current_state = next_state
                if is_accepting(current_state):
                    last_accepting_state = current_state
                    last_accepting_idx = scan_idx

                scan_idx += 1

            if last_accepting_state is not None:
                # Successfully recognized an accepted token pattern
                end_pos = last_accepting_idx + 1
                lexeme = text[start_pos:end_pos]
                token_type = get_token_type(last_accepting_state) or "UNKNOWN"

                tokens.append(Token(lexeme=lexeme, type=token_type, start=start_pos, end=end_pos))
                cursor = end_pos
            else:
                # Character could not be recognized by the DFA (unsupported or invalid)
                unknown_char = text[start_pos]
                tokens.append(
                    Token(lexeme=unknown_char, type="UNKNOWN", start=start_pos, end=start_pos + 1)
                )
                cursor = start_pos + 1

        return tokens


def tokenize(text: str) -> List[Token]:
    """
    Convenience module-level function to tokenize text.
    Provides direct access for Member 3 (UI visualizer) and Member 4 (evaluator).
    """
    lexer = Lexer()
    return lexer.tokenize(text)
