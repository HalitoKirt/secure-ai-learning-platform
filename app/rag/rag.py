import hashlib
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


DATA_FILE = Path("data/aws_notes.txt")
CHROMA_PATH = "storage/chroma"
COLLECTION_NAME = "aws_notes"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def create_chunk_id(text: str) -> str:
    """Create a stable unique ID for each chunk."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text into overlapping chunks.

    This prevents important context from being lost between chunks.
    """
    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def load_documents() -> None:
    """
    Load local notes into ChromaDB.

    Duplicate chunks are avoided by using stable hash-based IDs.
    """
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Missing data file: {DATA_FILE}")

    text = DATA_FILE.read_text(encoding="utf-8")
    chunks = chunk_text(text)

    added_count = 0

    existing = collection.get()
    existing_ids = set(existing["ids"])

    for chunk in chunks:
        chunk_id = create_chunk_id(chunk)

        if chunk_id in existing_ids:
            continue

        embedding = embedding_model.encode(chunk).tolist()

        collection.add(
            ids=[chunk_id],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{"source": str(DATA_FILE)}],
        )

        added_count += 1

    print(f"RAG loaded: {added_count} new chunks added, {len(chunks)} chunks processed.")


def query_docs(query: str, n_results: int = 3) -> list[str]:
    """
    Search the vector database for the most relevant chunks.
    """
    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    documents = results.get("documents", [[]])[0]

   # print("\n--- Retrieved Context ---")
   # for index, doc in enumerate(documents, start=1):
   #     print(f"[Chunk {index}] {doc[:300]}...")
   # print("--- End Retrieved Context ---\n")

    return documents
