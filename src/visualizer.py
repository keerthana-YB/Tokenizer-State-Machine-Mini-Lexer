# Member 3: DFA Visualization

import html
from src.lexer import tokenize
from src.dfa import (
    State,
    transition,
    classify_character,
    is_accepting,
)

# Color scheme for visual token chips (like OpenAI Tokenizer)
TOKEN_COLORS = {
    "IDENTIFIER": {
        "bg": "#E0E7FF",
        "border": "#818CF8",
        "text": "#1E1B4B",
        "label": "IDENTIFIER",
    },
    "NUMBER": {
        "bg": "#DCFCE7",
        "border": "#4ADE80",
        "text": "#064E3B",
        "label": "NUMBER",
    },
    "WHITESPACE": {
        "bg": "#FEF9C3",
        "border": "#FACC15",
        "text": "#713F12",
        "label": "WHITESPACE",
    },
    "PUNCTUATION": {
        "bg": "#FCE7F3",
        "border": "#F472B6",
        "text": "#831843",
        "label": "PUNCTUATION",
    },
    "UNKNOWN": {
        "bg": "#FEE2E2",
        "border": "#F87171",
        "text": "#7F1D1D",
        "label": "UNKNOWN",
    },
}


def render_color_tokens(text: str) -> str:
    """
    Render text as colored HTML token badges mimicking the OpenAI Tokenizer visualizer.
    """
    tokens = tokenize(text)
    if not tokens:
        return "<p><em>No tokens to display.</em></p>"

    html_parts = [
        '<div style="line-height: 2.6; padding: 14px; border: 1px solid #CBD5E1; '
        'border-radius: 8px; background-color: #F8FAFC; margin: 10px 0 20px 0;">'
    ]

    for token in tokens:
        color = TOKEN_COLORS.get(
            token.type,
            {"bg": "#F1F5F9", "border": "#94A3B8", "text": "#0F172A", "label": token.type},
        )
        display_val = html.escape(token.lexeme)
        if token.type == "WHITESPACE":
            display_val = display_val.replace(" ", "␣").replace("\t", "⇥").replace("\n", "↵\n")

        tooltip = f"{token.type} | Span: [{token.start}:{token.end}]"

        chip = (
            f'<span title="{tooltip}" style="'
            f'display: inline-block; '
            f'background-color: {color["bg"]}; '
            f'border: 1px solid {color["border"]}; '
            f'color: {color["text"]}; '
            f'border-radius: 6px; '
            f'padding: 3px 8px; '
            f'margin: 2px 3px; '
            f'font-family: monospace; '
            f'font-size: 14px; '
            f'box-shadow: 0 1px 2px rgba(0,0,0,0.05); '
            f'cursor: default;'
            f'">'
            f'<strong>{display_val}</strong> '
            f'<small style="font-size: 10px; opacity: 0.8; font-weight: 600;">'
            f'{color["label"]}</small>'
            f'</span>'
        )
        html_parts.append(chip)

    html_parts.append('</div>')
    return "".join(html_parts)


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
