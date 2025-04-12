import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from pathlib import Path

ARTICLE_DB_PATH = (
    Path(__file__).parent / ".." / "Datasets" / "prepared" / "article.db"
).resolve()
OUTPUT_FAISS_INDEX_PATH = (
    Path(__file__).parent / ".." / "Datasets" / "prepared" / "faiss_index.bin"
).resolve()
OUTPUT_ARTICLE_IDS_PATH = (
    Path(__file__).parent / ".." / "Datasets" / "prepared" / "article_ids.pkl"
).resolve()


# Setup
print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

# Fetch data
print("Fetching data from SQLite database...")
with sqlite3.connect(ARTICLE_DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT article_id, doc_full_name, doc_description FROM article")
    articles = cursor.fetchall()

# Prepare data
article_ids = []
texts = []
for article_id, name, desc in articles:
    text = f"{name} {desc}"
    texts.append(text)
    article_ids.append(article_id)

# Generate embeddings
embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=False,
).astype(np.float32)

# Handle NaNs
embeddings = np.nan_to_num(embeddings)

# Build FAISS index
faiss.omp_set_num_threads(1)
faiss_index = faiss.IndexHNSWFlat(embeddings.shape[1], 8)
faiss_index.hnsw.efConstruction = 32
faiss_index.hnsw.efSearch = 8
faiss_index.add(embeddings)

# Save index and IDs
print("Writing FAISS index and article IDs...")
faiss.write_index(faiss_index, str(OUTPUT_FAISS_INDEX_PATH))
with open(OUTPUT_ARTICLE_IDS_PATH, "wb") as f:
    pickle.dump(article_ids, f)

print("Done")
