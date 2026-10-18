
"""
Group 3: Tokenizer State Machine (Mini Lexer)
Member 1: DFA Logic

This module defines DFA states, character classes,
transitions, and accepting states.
"""

from enum import Enum, auto


class State(Enum):
    """States used by the DFA."""
    START = auto()
    IDENTIFIER = auto()
    INTEGER = auto()
    WHITESPACE = auto()
    PUNCTUATION = auto()
    DEAD = auto()


class CharacterClass(Enum):
    """Categories of input characters."""
    LETTER = auto()
    DIGIT = auto()
    WHITESPACE = auto()
    PUNCTUATION = auto()
    OTHER = auto()


# Punctuation and operators supported by this mini lexer.
PUNCTUATION_CHARS = set(".,;:!?(){}[]+-*/%=<>\"'&|^~#@")


def classify_character(char: str) -> CharacterClass:
    """Classify one input character."""
    if len(char) != 1:
        raise ValueError("Expected exactly one character")

    if char.isalpha() or char == "_":
        return CharacterClass.LETTER

    if char.isdigit():
        return CharacterClass.DIGIT

    if char.isspace():
        return CharacterClass.WHITESPACE

    if char in PUNCTUATION_CHARS:
        return CharacterClass.PUNCTUATION

    return CharacterClass.OTHER


# DFA transition table:
# TRANSITIONS[current_state][character_class] = next_state
TRANSITIONS = {
    State.START: {
        CharacterClass.LETTER: State.IDENTIFIER,
        CharacterClass.DIGIT: State.INTEGER,
        CharacterClass.WHITESPACE: State.WHITESPACE,
        CharacterClass.PUNCTUATION: State.PUNCTUATION,
        CharacterClass.OTHER: State.DEAD,
    },

    State.IDENTIFIER: {
        CharacterClass.LETTER: State.IDENTIFIER,
        CharacterClass.DIGIT: State.IDENTIFIER,
        CharacterClass.WHITESPACE: State.DEAD,
        CharacterClass.PUNCTUATION: State.DEAD,
        CharacterClass.OTHER: State.DEAD,
    },

    State.INTEGER: {
        CharacterClass.LETTER: State.DEAD,
        CharacterClass.DIGIT: State.INTEGER,
        CharacterClass.WHITESPACE: State.DEAD,
        CharacterClass.PUNCTUATION: State.DEAD,
        CharacterClass.OTHER: State.DEAD,
    },

    State.WHITESPACE: {
        CharacterClass.LETTER: State.DEAD,
        CharacterClass.DIGIT: State.DEAD,
        CharacterClass.WHITESPACE: State.WHITESPACE,
        CharacterClass.PUNCTUATION: State.DEAD,
        CharacterClass.OTHER: State.DEAD,
    },

    State.PUNCTUATION: {
        CharacterClass.LETTER: State.DEAD,
        CharacterClass.DIGIT: State.DEAD,
        CharacterClass.WHITESPACE: State.DEAD,
        CharacterClass.PUNCTUATION: State.DEAD,
        CharacterClass.OTHER: State.DEAD,
    },

    State.DEAD: {
        CharacterClass.LETTER: State.DEAD,
        CharacterClass.DIGIT: State.DEAD,
        CharacterClass.WHITESPACE: State.DEAD,
        CharacterClass.PUNCTUATION: State.DEAD,
        CharacterClass.OTHER: State.DEAD,
    },
}


# States in which a token pattern is accepted.
ACCEPTING_STATES = {
    State.IDENTIFIER,
    State.INTEGER,
    State.WHITESPACE,
    State.PUNCTUATION,
}


def transition(state: State, char: str) -> State:
    """Return the next DFA state for one character."""
    char_class = classify_character(char)
    return TRANSITIONS[state][char_class]


def is_accepting(state: State) -> bool:
    """Check whether the current state accepts a token."""
    return state in ACCEPTING_STATES


def get_token_type(state: State) -> str | None:
    """Return the token type for an accepting state."""
    token_types = {
        State.IDENTIFIER: "IDENTIFIER",
        State.INTEGER: "NUMBER",
        State.WHITESPACE: "WHITESPACE",
        State.PUNCTUATION: "PUNCTUATION",
    }
    return token_types.get(state)
