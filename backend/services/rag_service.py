from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from backend.utils.data_loader import load_single_file
from backend.utils.search import search
from backend.utils.vectorstore import build_save_vectorstore
from backend.config.settings import settings

llm = ChatGroq(model='openai/gpt-oss-120b', temperature=0.2,
               max_tokens=500, api_key=settings.GROQ_API_KEY)


def ingest_file(file_path: str) -> int:
    """
    Upload pipeline:
    file_path → load → split → embed → FAISS → disk
    Called by upload_routes.py after saving the file.
    Returns chunk count so the API can return it to frontend.
    """
    documents = load_single_file(file_path)
    chunk_count = build_save_vectorstore(documents)
    return chunk_count


def query_document(question: str, top_k: int = 5) -> dict:
    """
    Query pipeline:
    question → search FAISS → build prompt → LLM → answer
    Called by rag_routes.py on every user question.
    """

    relevant_chunks = search(question, top_k=top_k)

    if not relevant_chunks:
        return {
            "answer": "No relevant content found in the document.",
            "source_chunks": []
        }

    context = "\n\n".join(relevant_chunks)

    messages = [
        SystemMessage(content="""
You are an intelligent document assistant. 
Your job is to answer questions based strictly on the provided document context.

Follow these rules for every response:
- Answer only from the context provided
- If the answer is not in the context say exactly:
  "I could not find this information in the uploaded document."
- Format your answers clearly:
  * For explanations    → write in clear paragraphs
  * For steps/process  → use numbered points (1. 2. 3.)
  * For comparisons    → use tabular format with structured points
  * For definitions    → one clear paragraph
  * For lists of items → use bullet points
- Keep answers concise but complete
- Do not make up information
- Do not use outside knowledge
        """),
        HumanMessage(content=f"""
Context from document:
──────────────────────
{context}
──────────────────────

Question: {question}

Answer:
        """)
    ]

    response = llm.invoke(messages)

    return {
        "answer": response.content.strip(),
        "source_chunks": relevant_chunks
    }


#Code for checking the working 
if __name__ == "__main__":
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    pdf_path = BASE_DIR / "data" / "uploads" / "Jaya_CV.pdf"

    print("\n[TEST] Starting ingestion...\n")

    chunk_count = ingest_file(str(pdf_path))

    print(f"\n[TEST] Indexed {chunk_count} chunks\n")

    question = "What skills does the candidate have?"

    print(f"\n[TEST] Question: {question}\n")

    result = query_document(question)

    print("\n========== ANSWER ==========\n")

    print(result["answer"])

    print("\n====== SOURCE CHUNKS ======\n")

    for i, chunk in enumerate(result["source_chunks"], 1):

        print(f"\n--- Chunk {i} ---\n")

        print(chunk[:500])
