import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# === ChromaDB Config ===
CHROMA_DIR = "chroma_store"
COLLECTION_NAME = "rag_pdf"
RESET_COLLECTION = False  # 🔁 Set to True if you want to wipe collection on every run

# === Initialize ChromaDB client ===
client = chromadb.PersistentClient(path=CHROMA_DIR)

# === Define embedding model ===
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# === Get or reset the collection ===
if COLLECTION_NAME in [col.name for col in client.list_collections()]:
    if RESET_COLLECTION:
        client.delete_collection(COLLECTION_NAME)
        collection = client.create_collection(name=COLLECTION_NAME, embedding_function=embedding_function)
    else:
        collection = client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_function)
else:
    collection = client.create_collection(name=COLLECTION_NAME, embedding_function=embedding_function)
