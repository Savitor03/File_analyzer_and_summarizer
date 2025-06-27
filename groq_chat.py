import streamlit as st

# === Update & Store Chat History ===
def update_chat_history(question, answer):
    st.session_state.chat_history.append((question, answer))

# === Display Chat Interface with Delete Option ===
def display_chat():
    for i, (q, a) in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.markdown(f"**You:** {q}")

        with st.chat_message("assistant"):
            col1, col2 = st.columns([0.95, 0.05])
            with col1:
                st.markdown(f"**PDF-Genius:** {a}")
            with col2:
                if st.button("❌", key=f"del_{i}", help="Delete this QA"):
                    del st.session_state.chat_history[i]
                    st.experimental_rerun()
