import chromadb
from sentence_transformers import SentenceTransformer

# Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create in-memory DB
client = chromadb.PersistentClient(path="storage/chroma")
collection = client.create_collection(name="aws_notes")

def load_documents():
    with open("data/aws_notes.txt", "r") as f:
        text = f.read()

    chunks = text.split("\n")

    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()

        collection.add(
            ids=[str(i)],
            documents=[chunk],
            embeddings=[embedding]
        )

def query_docs(query):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    return results["documents"][0]
