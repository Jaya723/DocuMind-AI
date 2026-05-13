from typing import List, Any
from backend.utils.vectorstore import load_vectorstore


def search(query: str, top_k: int = 5) -> List[str]:
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search(query, k=top_k)
    chunks = [doc.page_content for doc in results]
    print(
        f"Search results for query: '{query}'. Found {len(chunks)} relevant chunks.")
    return chunks


def search_with_scores(query: str, top_k: int = 5) -> List[dict]:
    """
    Same as search_documents but includes relevance scores
    and source page info. Use this for debugging or if you
    want to show the user where the answer came from.

    Score is L2 distance — lower = more relevant.
    Typically: score < 1.0 = very relevant
               score > 2.0 = loosely related
    """
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search_with_score(query, k=top_k)

    return [
        {
            "content": doc.page_content,
            "score": round(float(score), 4),
            "page": doc.metadata.get("page", "unknown"),
            "source": doc.metadata.get("source", "unknown")
        }
        for doc, score in results
    ]
