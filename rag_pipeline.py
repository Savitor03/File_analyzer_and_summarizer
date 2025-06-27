import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os
import requests
from utils import chunk_text

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# === ChromaDB Setup ===
CHROMA_DIR = "chroma_store"

client = chromadb.PersistentClient(path=CHROMA_DIR)
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def get_or_create_collection(session_name):
    collection_name = f"session_{session_name}"
    existing_collections = [col.name for col in client.list_collections()]
    if collection_name in existing_collections:
        return client.get_collection(name=collection_name, embedding_function=embedding_function)
    else:
        return client.create_collection(name=collection_name, embedding_function=embedding_function)

def ingest_pdf(text, file_name, session_name=None):
    if not session_name:
        return "❌ Session name is required to ingest."

    collection = get_or_create_collection(session_name)

    # Chunk and store
    chunks = chunk_text(text)
    documents = [chunk for chunk in chunks]
    metadatas = [{"pdf": file_name, "chunk": i, "session": session_name} for i in range(len(chunks))]
    ids = [f"{file_name}_{i}" for i in range(len(chunks))]

    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    return True

def answer_query(query, top_k=3, model_name="llama3-8b-8192", session_name=None):
    if not session_name:
        return "❌ No session selected. Please save or load a session first."

    collection = get_or_create_collection(session_name)

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where={"session": session_name}
    )

    docs = results.get("documents", [[]])[0]
    sources = results.get("metadatas", [[]])[0]

    if not docs:
        return "No relevant context found for this session."

    context = "\n".join(
        [f"[{meta['pdf']} - Chunk {meta['chunk']}] {doc}" for doc, meta in zip(docs, sources)]
    )

    prompt = f"""Use the context below to answer the question clearly, accurately, and helpfully.

Context:
{context}

Question:
{query}

Answer:"""

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("❌ GROQ API Error:", e)
        return "Error generating answer. Please check the API key or connection."
