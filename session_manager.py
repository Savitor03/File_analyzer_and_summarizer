import os
import json
import chromadb
from chromadb.utils import embedding_functions

# === ChromaDB Setup ===
CHROMA_DIR = "chroma_store"
client = chromadb.PersistentClient(path=CHROMA_DIR)
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

SESSION_DIR = "sessions"
os.makedirs(SESSION_DIR, exist_ok=True)

def save_session(session_name, chat_history, pdf_names):
    """Save chat history and uploaded file names to a session file."""
    session_data = {
        "chat_history": chat_history,
        "pdf_names": pdf_names
    }
    path = os.path.join(SESSION_DIR, f"{session_name}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Failed to save session '{session_name}': {e}")

def load_session(session_name):
    """Load session file and return its data."""
    path = os.path.join(SESSION_DIR, f"{session_name}.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Failed to load session '{session_name}': {e}")
    return {"chat_history": [], "pdf_names": []}

def list_sessions():
    """List all saved sessions without .json extension."""
    try:
        return [f[:-5] for f in os.listdir(SESSION_DIR) if f.endswith(".json")]
    except Exception as e:
        print(f"❌ Failed to list sessions: {e}")
        return []

def delete_session(session_name):
    """Delete a saved session file and corresponding ChromaDB collection."""
    path = os.path.join(SESSION_DIR, f"{session_name}.json")
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            print(f"❌ Failed to delete session '{session_name}': {e}")

    # Delete associated ChromaDB collection
    collection_name = f"session_{session_name}"
    try:
        existing_collections = [col.name for col in client.list_collections()]
        if collection_name in existing_collections:
            client.delete_collection(name=collection_name)
            print(f"🗑️ Deleted ChromaDB collection for session: {collection_name}")
    except Exception as e:
        print(f"❌ Failed to delete ChromaDB collection '{collection_name}': {e}")
