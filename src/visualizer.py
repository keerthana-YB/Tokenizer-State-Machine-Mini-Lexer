# Member 3: DFA Visualization

from src.lexer import tokenize
from src.dfa import (
    State,
    transition,
    classify_character,
    is_accepting,
)


def get_token_table(text: str) -> list[dict]:
    tokens = tokenize(text)

    return [
        {
            "Lexeme": token.lexeme,
            "Token Type": token.type,
            "Start": token.start,
            "End": token.end,
        }
        for token in tokens
    ]


def trace_dfa(text: str) -> list[dict]:
    steps = []

    for token in tokenize(text):
        state = State.START

        for position in range(token.start, token.end):
            character = text[position]
            next_state = transition(state, character)
            char_class = classify_character(character)

            steps.append({
                "Position": position,
                "Character": repr(character),
                "Character Class": getattr(
                    char_class, "name", str(char_class)
                ),
                "From State": getattr(state, "name", str(state)),
                "To State": getattr(next_state, "name", str(next_state)),
                "Accepting": is_accepting(next_state),
                "Token": token.lexeme,
                "Token Type": token.type,
            })

            state = next_state

    return steps


def format_trace(text: str) -> str:
    steps = trace_dfa(text)

    if not steps:
        return "No characters to process."

    columns = [
        "Position",
        "Character",
        "Character Class",
        "From State",
        "To State",
        "Accepting",
    ]

    lines = [" | ".join(columns)]

    for step in steps:
        lines.append(
            " | ".join(str(step[column]) for column in columns)
        )

    return "\n".join(lines)

