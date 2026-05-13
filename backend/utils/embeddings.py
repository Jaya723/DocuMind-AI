from typing import List, Any
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

_embeddings = None


def get_embeddings() -> HuggingFaceEmbeddings:
    # Used for making the model object so that no need to upload the model again and again for every file. It will be loaded once and then used for all the files.
    global _embeddings

    if _embeddings is None:
        print(f"Loading model: {MODEL_NAME}")
        _embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
        print("Embedding Model ready")

    return _embeddings


def split_documents(documents: List[Any]) -> List[Any]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks")
    return chunks


def embed_documents(chunks: List[Any]):
    embeddings = get_embeddings()
    texts = [chunk.page_content for chunk in chunks]
    vectors = embeddings.embed_documents(texts)
    print(f"Created {len(vectors)} embeddings")
    return vectors


#code to check if the funttions are working properly with a sample file
if __name__ == "__main__":
    from data_loader import load_single_file
    BASE_DIR = Path(__file__).parent.parent.parent
    uploaded_file = BASE_DIR / "data" / "uploads" / "Jaya_CV.pdf"
    docs = load_single_file(uploaded_file)
    chunks = split_documents(docs)
    print(chunks)
    print(embed_documents(chunks))
