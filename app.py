# Member 3: Streamlit Interface

import streamlit as st
import pandas as pd

from src.visualizer import get_token_table, trace_dfa


st.set_page_config(
    page_title="Tokenizer State Machine",
    page_icon="🔎",
    layout="wide"
)

st.title("Tokenizer State Machine - Mini Lexer")
st.write("Visualize how a Deterministic Finite Automaton processes input.")

text = st.text_area(
    "Enter text to tokenize",
    value="count = 123;",
    height=150
)

if st.button("Tokenize"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        try:
            tokens = get_token_table(text)

            st.subheader("Token Table")

            if tokens:
                st.dataframe(
                    pd.DataFrame(tokens),
                    use_container_width=True
                )
            else:
                st.info("No tokens were produced.")

            st.subheader("DFA Transition Trace")
            steps = trace_dfa(text)

            if steps:
                st.dataframe(
                    pd.DataFrame(steps),
                    use_container_width=True
                )
            else:
                st.info("No transitions to display.")

        except Exception as error:
            st.error(f"Unable to process input: {error}")
            st.info("Check that the lexer and DFA implementations are complete.")
