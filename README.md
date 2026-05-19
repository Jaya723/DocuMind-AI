# DocuMind AI 📄🤖

A full-stack Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask questions about them using AI.

DocuMind AI supports multiple document formats, performs semantic search using FAISS vector storage, and generates context-aware answers using LLMs.
____________________________________________________________________________________________________________________________________________________________

# Features 🚀

* User Authentication (JWT-based)
* Secure Signup & Login
* Upload and index documents
* Supports multiple file formats:
  * PDF
  * TXT
  * CSV
  * DOCX
* Semantic search with FAISS
* AI-powered document question answering
* Chat history storage
* Persistent MySQL database
* FastAPI backend
* Streamlit frontend
* Modular backend architecture
____________________________________________________________________________________________________________________________________________________________

# Tech Stack 🛠️

## Backend

* FastAPI
* SQLAlchemy
* MySQL
* LangChain
* FAISS
* HuggingFace Embeddings
* Groq LLM
* JWT Authentication
* Passlib (bcrypt)
____________________________________________________________________________________________________________________________________________________________

## Frontend

* Streamlit
____________________________________________________________________________________________________________________________________________________________

## AI / RAG

* RecursiveCharacterTextSplitter
* all-MiniLM-L6-v2 embeddings
* Vector similarity search
__________________________________________________________________________________________________________________________________________________________

# How It Works ⚙️

1. User signs up or logs in.
2. JWT token is generated for authentication.
3. User uploads a document.
4. Document is:

   * loaded
   * chunked
   * converted into embeddings
   * stored in FAISS vector database
5. User asks questions about the document.
6. Relevant chunks are retrieved using semantic similarity.
7. LLM generates a context-aware answer.
8. Chat history is stored in MySQL.
____________________________________________________________________________________________________________________________________________________________

# Supported File Types 📄

| File Type | Loader Used    |
| --------- | -------------- |
| PDF       | PyPDFLoader    |
| TXT       | TextLoader     |
| CSV       | CSVLoader      |
| DOCX      | Docx2txtLoader |
____________________________________________________________________________________________________________________________________________________________

# API Routes 🌐

## Authentication Routes

| Method | Endpoint       | Description       |
| ------ | -------------- | ----------------- |
| POST   | `/auth/signup` | Register new user |
| POST   | `/auth/login`  | Login user        |

## Upload Routes

| Method | Endpoint   | Description               |
| ------ | ---------- | ------------------------- |
| POST   | `/upload/` | Upload and index document |

## RAG Routes

| Method | Endpoint       | Description                 |
| ------ | -------------- | --------------------------- |
| POST   | `/rag/query`   | Ask question about document |
| GET    | `/rag/history` | Fetch chat history          |
| DELETE | `/rag/history` | Clear chat history          |

____________________________________________________________________________________________________________________________________________________________

# API Documentation 📘

FastAPI automatically generates Swagger docs:

# Example Workflow 💡

1. Create account
2. Upload document
3. Ask questions like:
   * "Summarize this document"
   * "What are the key points?"
   * "Who is mentioned in the document?"
4. Receive AI-generated answers
 ____________________________________________________________________________________________________________________________________________________________

# Screenshots 📸
<img width="1202" height="807" alt="Screenshot 2026-05-20 012539" src="https://github.com/user-attachments/assets/e727cc8f-a742-45f8-a53f-f294afccd646" />
<img width="977" height="763" alt="Screenshot 2026-05-20 012628" src="https://github.com/user-attachments/assets/d5afc513-5ddb-422a-88f2-49c6e34de822" />
<img width="1777" height="791" alt="Screenshot 2026-05-20 013121" src="https://github.com/user-attachments/assets/209e3d2b-54b0-43d7-9ff5-22cf009f8b07" />
<img width="1697" height="862" alt="Screenshot 2026-05-20 012829" src="https://github.com/user-attachments/assets/a210e701-dd46-4a43-ac73-baf10eb48521" />
<img width="1733" height="876" alt="Screenshot 2026-05-20 012941" src="https://github.com/user-attachments/assets/bd72a2da-86b7-49c4-97c2-76494ef97100" />
<img width="1727" height="847" alt="Screenshot 2026-05-20 013031" src="https://github.com/user-attachments/assets/878480a1-8145-4a2e-976a-7a8e2582dc77" />
____________________________________________________________________________________________________________________________________________________________

# Future Improvements 🚧

* Multi-document support
* Conversation memory
* Streaming responses
* Role-based authentication
* Cloud deployment
* Better UI/UX
* Source citations in answers
___________________________________________________________________________________________________________________________________________________________

# Author 👨‍💻

Jaya Agarwal
__________________________________________________________________________________________________________________________________________________________


# License 📄

This project is for learning and educational purposes.
