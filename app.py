import streamlit as st
from utils import extract_text_from_file, get_stats
from rag_pipeline import ingest_pdf, answer_query
from groq_chat import update_chat_history
from session_manager import save_session, load_session, list_sessions, delete_session
import os

# === Setup Directories ===
os.makedirs("uploads", exist_ok=True)
os.makedirs("sessions", exist_ok=True)

# === Page Setup ===
st.set_page_config(page_title="📄 File Analyzer", layout="wide")
st.title("📄 File Analyzer - Multi-file Summarizer & RAG Chat")

# === Session Initialization ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = None
if "current_session" not in st.session_state:
    st.session_state.current_session = None
    
    


# === Sidebar ===

with st.sidebar:
    
    
    st.subheader("Session Manager")
    sessions = list_sessions()
    selected_session = st.selectbox("Load Session", ["-- New Session --"] + sessions)

    if selected_session == "-- New Session --":
        st.session_state.chat_history = []
        st.session_state.selected_chat = None
        st.session_state.current_session = f"temp_session_{len(sessions)+1}"
    else:
        data = load_session(selected_session)
        st.session_state.chat_history = data.get("chat_history", [])
        st.session_state.selected_chat = None
        st.session_state.current_session = selected_session


    new_session_name = st.text_input("Save Session As")
    if st.button("Save Session"):
        if new_session_name.strip():
            save_session(new_session_name.strip(), st.session_state.chat_history, [])
            st.session_state.current_session = new_session_name.strip()
        else:
            st.warning("Please enter a valid session name.")

    
    st.header("📁 Upload Files")
    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, PPTX, TXT, or MD files",
        type=["pdf", "docx", "pptx", "txt", "md"],
        accept_multiple_files=True
    )
    if uploaded_files:
        if not st.session_state.current_session:
            st.warning("⚠️ Please save or load a session before uploading files.")
        else:
            for file in uploaded_files:
                file_path = f"uploads/{file.name}"
                with open(file_path, "wb") as f:
                    f.write(file.read())

                text = extract_text_from_file(file_path)
                if text.strip():
                    ingest_pdf(text, file.name, session_name=st.session_state.current_session)

                try:
                    os.remove(file_path)
                except Exception as e:
                    st.warning(f"Could not delete file {file.name}: {e}")

            st.success(f"Ingested {len(uploaded_files)} file(s)")
            
    delete_selected = st.selectbox("Delete Session", ["-- Select Session --"] + sessions)
    if st.button("Delete Session"):
        if delete_selected != "-- Select Session --":
            delete_session(delete_selected)
            st.success(f"Deleted session: {delete_selected}")
            st.rerun()
            
    st.markdown("---")
    st.subheader("Model Selection")
    selected_model = st.selectbox("Choose model:", ["llama3-8b-8192", "mixtral-8x7b-32768"], index=0)
    st.session_state.selected_model = selected_model

    st.markdown("---")

    export_name = f"{st.session_state.current_session or 'chat'}.txt"

    st.download_button(
        "Export Chat",
        "\n\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.chat_history]),
        file_name=export_name
)



    st.markdown("---")
    st.subheader("Summarize Content")
    if st.button("Summarize All"):
        if st.session_state.current_session:
            with st.spinner("Summarizing..."):
                summary = answer_query("Summarize the entire content...", model_name=st.session_state.selected_model, session_name=st.session_state.current_session)
            st.markdown("### Summary")
            st.write(summary)
        else:
            st.warning("Please select or save a session before summarizing.")

# === Chat Input ===
query = st.chat_input("Ask a question about your uploaded files...")
if query:
    if not st.session_state.current_session:
        st.warning("⚠️ Please save a session before chatting.")
    else:
        with st.spinner("Thinking..."):
            answer = answer_query(query, model_name=st.session_state.selected_model, session_name=st.session_state.current_session)
            update_chat_history(query, answer)
            st.session_state.selected_chat = len(st.session_state.chat_history) - 1

            save_session(st.session_state.current_session, st.session_state.chat_history, [])

# === Chat Viewer ===
if st.session_state.chat_history:
    st.markdown("## Chat History")
    for i, (q, a) in enumerate(st.session_state.chat_history):
        with st.expander(f"Q{i+1}: {q}", expanded=(i == st.session_state.selected_chat)):
            st.markdown(f"**You:** {q}")
            st.markdown(f"**Me:** {a}")
            if st.button("❌ Delete", key=f"delete_chat_{i}"):
                del st.session_state.chat_history[i]
                if st.session_state.selected_chat == i:
                    st.session_state.selected_chat = None
                elif st.session_state.selected_chat and st.session_state.selected_chat > i:
                    st.session_state.selected_chat -= 1
                save_session(st.session_state.current_session, st.session_state.chat_history, [])
                st.rerun()
