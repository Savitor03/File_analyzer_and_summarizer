
# 📄 PDF-Genius: Multi-File Summarizer & RAG Q&A App

PDF-Genius is a powerful Streamlit app that allows you to:
- Upload documents (PDF, DOCX, PPTX, TXT, MD)
- Automatically chunk and store text with ChromaDB
- Ask questions via a Retrieval-Augmented Generation (RAG) pipeline
- Choose between `llama3` and `mixtral` models (via Groq API)
- Summarize entire documents in one click
- Manage and persist multiple chat sessions

---

## 🚀 Features

✅ Supports multiple file formats: `PDF`, `DOCX`, `PPTX`, `TXT`, `MD`  
✅ Uses `InstructorEmbedding` for semantic search  
✅ Fast LLM answers powered by Groq's `llama3-8b-8192` or `mixtral-8x7b-32768`  
✅ Persistent session management: save, load, and delete chats  
✅ Smart chat history with context-aware answers  
✅ Clean, intuitive Streamlit UI  

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/pdf-genius.git
cd pdf-genius
```

### 2. Create `.env` file

Create a `.env` file in the root with the following content:

```
GROQ_API_KEY=your_groq_api_key_here
```
> Make sure `.env` is listed in `.gitignore`.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## 🧠 Tech Stack

- **Frontend/UI**: Streamlit  
- **LLM Interface**: Groq API (LLaMA 3, Mixtral)  
- **Vector Store**: ChromaDB  
- **Embeddings**: InstructorEmbedding  
- **File Parsing**: PyMuPDF, python-docx, python-pptx  

---

## 📂 Project Structure

```
├── app.py               # Main Streamlit UI
├── rag_pipeline.py      # RAG logic (embedding, querying, answering)
├── utils.py             # File extraction, stats
├── groq_chat.py         # Chat display + update
├── session_manager.py   # Save/load/delete sessions
├── uploads/             # Temp uploaded files
├── sessions/            # JSON chat session files
├── requirements.txt
├── .env
└── .gitignore
```

---

## 🧪 Sample Queries

- "Summarize the uploaded document."
- "What is the key point in Slide 4 of the presentation?"
- "Explain the second paragraph of the DOCX file."

---

## 📤 Export Options

You can export:
- Full chat history as `.txt`
- Individual sessions saved with unique names

---

## 👥 Author

Made by KAVIARASAN M ✨  


---

> This project uses Groq API for blazing fast inference. Make sure to generate a key from [https://console.groq.com](https://console.groq.com)
