# Group 3: Tokenizer State Machine (Mini Lexer)
# Streamlit Web Application

import streamlit as st
import pandas as pd

from src.visualizer import get_token_table, trace_dfa, render_color_tokens
from src.comparison import compare_token_counts


st.set_page_config(
    page_title="Tokenizer State Machine - Mini Lexer",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Tokenizer State Machine (Mini Lexer)")
st.write(
    "Explore how a **Deterministic Finite Automaton (DFA)** tokenizes text character-by-character "
    "and compare the token boundaries with **OpenAI GPT (tiktoken)**."
)

# Text Input Section
text = st.text_area(
    "Enter text to tokenize:",
    value="Hello world! 42 tokens.",
    height=100
)

col1, col2 = st.columns([1, 5])
with col1:
    run_btn = st.button("🚀 Tokenize", type="primary", use_container_width=True)

if text:
    try:
        # 1. Color-Coded Token Visualization (Like OpenAI Tokenizer)
        st.subheader("🎨 Color-Coded Token Boundaries")
        st.write("Each token type is displayed with a distinct color tag. Hover over a token to see its character offsets:")
        st.markdown(render_color_tokens(text), unsafe_allow_html=True)

        # 2. Comparison with OpenAI GPT-4 (tiktoken)
        st.subheader("🤖 Token Count Comparison: DFA Lexer vs GPT-4 (tiktoken)")
        comparison = compare_token_counts(text)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Mini-Lexer DFA Tokens", comparison.lexer_token_count)
        m2.metric("GPT-4 (tiktoken) Tokens", comparison.gpt_token_count)
        m3.metric("Difference", f"{comparison.difference:+d}")

        if comparison.difference < 0:
            st.caption(
                "💡 **Why does GPT have fewer tokens?** "
                "OpenAI's BPE tokenizer attaches leading whitespace directly to words (e.g. `' world'`), "
                "whereas a formal DFA lexer treats whitespace as standalone delimiter tokens."
            )

        # 3. Token Table
        st.subheader("📋 Token Table")
        tokens = get_token_table(text)
        if tokens:
            st.dataframe(pd.DataFrame(tokens), use_container_width=True)
        else:
            st.info("No tokens produced.")

        # 4. DFA Transition Trace
        st.subheader("⚙️ Step-by-Step DFA Transition Trace")
        st.write("Inspect how the automaton transitions between states for each character:")
        steps = trace_dfa(text)
        if steps:
            st.dataframe(pd.DataFrame(steps), use_container_width=True)
        else:
            st.info("No transitions to display.")

    except Exception as error:
        st.error(f"Unable to process input: {error}")
        st.info("Check that the lexer and DFA implementations are complete.")

# 5. Theoretical DFA Diagram Expander
with st.expander("📖 View DFA State Machine Specification"):
    st.markdown("""
    ### State Descriptions:
    - **q0 (START):** Initial state awaiting the first character of a token.
    - **q1 (IDENTIFIER):** Consumes alphabetic characters, underscores, and subsequent digits.
    - **q2 (INTEGER):** Consumes numeric digits (0–9).
    - **q3 (WHITESPACE):** Consumes spaces, tabs, and newlines.
    - **q4 (PUNCTUATION):** Matches individual punctuation marks and operators.
    - **qd (DEAD):** Trap state signaling a token boundary (Maximal Munch emission).
    
    ```mermaid
    flowchart LR
        start([Start]) --> q0((q0: START))
        q0 -->|LETTER| q1(((q1: IDENTIFIER)))
        q0 -->|DIGIT| q2(((q2: INTEGER)))
        q0 -->|WHITESPACE| q3(((q3: WHITESPACE)))
        q0 -->|PUNCTUATION| q4(((q4: PUNCTUATION)))
        q0 -->|OTHER| qd((qd: DEAD))
        q1 -->|LETTER or DIGIT| q1
        q2 -->|DIGIT| q2
        q3 -->|WHITESPACE| q3
        q1 -->|WHITESPACE, PUNCT, OTHER| qd
        q2 -->|LETTER, WHITESP, PUNCT, OTHER| qd
        q3 -->|LETTER, DIGIT, PUNCT, OTHER| qd
        q4 -->|Any next character| qd
        qd -->|Any input| qd
    ```
    """)
