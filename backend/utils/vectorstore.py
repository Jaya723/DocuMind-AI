import os
from typing import List, Any
from langchain_community.vectorstores import FAISS
from backend.utils.embeddings import get_embeddings, split_documents

FAISS_PATH = "data/faiss_index"


def build_save_vectorstore(documents: List[Any]) -> int:
    os.makedirs("data", exist_ok=True)
    chunks = split_documents(documents)

    if not chunks:
        raise ValueError("No content in the uploaded document")
    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(FAISS_PATH)

    print(f"Vectorstore built and saved at {FAISS_PATH}")
    print(f"Number of chunks in vectorstore: {len(chunks)}")

    return len(chunks)


def load_vectorstore() -> FAISS:
    """ load the vectorstore from disk for the retrieval part."""
    if not os.path.exists(FAISS_PATH):
        raise FileNotFoundError(
            f"Vectorstore not found at {FAISS_PATH}. Please upload a document first.")

    embeddings = get_embeddings()
    vectorstore = FAISS.load_local(
        FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    print(f"Vectorstore loaded from {FAISS_PATH}")
    return vectorstore
