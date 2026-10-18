
# Group 3: Tokenizer State Machine (Mini Lexer)
## DFA Transition Table — Member 1

## 1. Objective

The Deterministic Finite Automaton (DFA) identifies character patterns
used by our mini lexer for tokenization in an LLM-related application.

## 2. Character Classes

| Character Class | Description | Examples |
|---|---|---|
| LETTER | Alphabetic characters and underscore | a, Z, _ |
| DIGIT | Numeric digits | 0, 7, 9 |
| WHITESPACE | Spaces, tabs, and newlines | space, \t, \n |
| PUNCTUATION | Supported punctuation and operators | ; + ( ) = |
| OTHER | Characters outside supported classes | unsupported symbols |

## 3. DFA States

| State | Description | Accepting? |
|---|---|---|
| START | Initial state | No |
| IDENTIFIER | Recognizes identifier patterns | Yes |
| INTEGER | Recognizes integer number patterns | Yes |
| WHITESPACE | Recognizes whitespace sequences | Yes |
| PUNCTUATION | Recognizes one punctuation character | Yes |
| DEAD | Invalid continuation or unsupported input | No |

## 4. Transition Table

Each cell gives the next state for the current state and input class.

| Current State | LETTER | DIGIT | WHITESPACE | PUNCTUATION | OTHER |
|---|---|---|---|---|---|
| START | IDENTIFIER | INTEGER | WHITESPACE | PUNCTUATION | DEAD |
| IDENTIFIER | IDENTIFIER | IDENTIFIER | DEAD | DEAD | DEAD |
| INTEGER | DEAD | INTEGER | DEAD | DEAD | DEAD |
| WHITESPACE | DEAD | DEAD | WHITESPACE | DEAD | DEAD |
| PUNCTUATION | DEAD | DEAD | DEAD | DEAD | DEAD |
| DEAD | DEAD | DEAD | DEAD | DEAD | DEAD |

## 5. Accepting States

The accepting states are:

- IDENTIFIER
- INTEGER
- WHITESPACE
- PUNCTUATION

The DEAD state is not accepting.

## 6. Example: Recognizing an Identifier

Input: `count42`

| Input Character | Character Class | State |
|---|---|---|
| Start | — | START |
| c | LETTER | IDENTIFIER |
| o | LETTER | IDENTIFIER |
| u | LETTER | IDENTIFIER |
| n | LETTER | IDENTIFIER |
| t | LETTER | IDENTIFIER |
| 4 | DIGIT | IDENTIFIER |
| 2 | DIGIT | IDENTIFIER |

Final result: `IDENTIFIER("count42")`

## 7. Example: Tokenizing an Expression

Input: `count = 123;`

Expected token sequence:

- IDENTIFIER("count")
- PUNCTUATION("=")
- NUMBER("123")
- PUNCTUATION(";")

Whitespace can be skipped by the lexer.

## 8. Relationship Between DFA and Lexer

1. The lexer reads the input one character at a time.
2. The DFA classifies each character and determines state transitions.
3. The lexer collects characters while a token pattern is valid.
4. When a token boundary is encountered, the lexer emits the completed token.
5. The lexer processes the boundary character again from START when needed.

## 9. Limitations

- Integer numbers are supported; decimal numbers need additional states or rules.
- Quoted strings and comments are not yet implemented.
- The lexer must handle token boundaries and invalid input explicitly.
- This DFA is a simplified educational model, not a complete LLM tokenizer.
