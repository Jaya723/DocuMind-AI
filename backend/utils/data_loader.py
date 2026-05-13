# Making the data ingestion pipeline for different types of documents like PDF, Text, CSV, and DOCX.
from pathlib import Path
from typing import List, Any
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, Docx2txtLoader

LOADERS = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".csv": CSVLoader,
    ".docx": Docx2txtLoader,
}


def load_single_file(file_path: str)->List[Any]:
    path = Path(file_path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")

    ext = path.suffix.lower()

    if ext not in LOADERS:
        raise ValueError(
            f"Unsupported file type: {ext}. Supported types are: {', '.join(LOADERS.keys())}")

    try:
        loader_class = LOADERS[ext]
        loader = loader_class(str(path))
        documents = loader.load()

        for doc in documents:
            doc.metadata["source_file"] = path.name
            doc.metadata["file_type"] = ext

        print(f"Loaded {len(documents)} document pages")
        return documents

    except Exception as e:
        raise RuntimeError(f"Error loading file {file_path}: {str(e)}")


# Code for checking the function with a sample file
if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent.parent.parent
    uploaded_file = BASE_DIR / "data" / "uploads" / "Jaya_CV.pdf"
    docs = load_single_file(uploaded_file)
    print(docs)
