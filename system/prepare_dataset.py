import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from usearch.index import Index
import pickle
from pathlib import Path

ARTICLE_DB_PATH = (
    Path(__file__).parent / "datasets" / "prepared" / "article.db"
).resolve()
OUTPUT_USEARCH_INDEX_PATH = (
    Path(__file__).parent / "datasets" / "prepared" / "usearch_index.usearch"
).resolve()
OUTPUT_ARTICLE_IDS_PATH = (
    Path(__file__).parent / "datasets" / "prepared" / "article_ids.pkl"
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

# Build USearch index
print("Building USearch index...")
dimensions = embeddings.shape[1]
usearch_index = Index(
    ndim=dimensions,
    metric="cos",  # Cosine similarity
    connectivity=8,
)

# Add embeddings to the index
for i, embedding in enumerate(embeddings):
    usearch_index.add(i, embedding)

# Save index and IDs
print("Writing USearch index and article IDs...")
usearch_index.save(OUTPUT_USEARCH_INDEX_PATH)
with open(OUTPUT_ARTICLE_IDS_PATH, "wb") as f:
    pickle.dump(article_ids, f)

print("Done")
