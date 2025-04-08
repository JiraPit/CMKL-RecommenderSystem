import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import time

# Setup
db_name = "article.db"
start = time.time()
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
print("Model loaded.")
print("Time taken:", time.time() - start)

# Fetch data
with sqlite3.connect(db_name) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT article_id, doc_body, doc_full_name, doc_description FROM article")
    articles = cursor.fetchall()

# Generate embeddings
article_ids = []
embeddings = []

for article_id, body, name, desc in articles:
    article_ids.append(article_id)
    combined_text = f"{body} {name} {desc}"
    embedding = model.encode([combined_text], convert_to_numpy=True, show_progress_bar=False)
    embeddings.append(embedding)

combined_embeddings = np.vstack(embeddings).astype(np.float32)
print(f"Embeddings shape: {combined_embeddings.shape}")

# Handle NaNs/Infs
combined_embeddings = np.nan_to_num(combined_embeddings, 0)

# Build FAISS index
faiss.omp_set_num_threads(1)
index = faiss.IndexHNSWFlat(combined_embeddings.shape[1], 8)
index.hnsw.efConstruction = 32
index.hnsw.efSearch = 8
index.add(combined_embeddings)

# Save index and IDs
faiss.write_index(index, "faiss_hnsw_index.bin")
with open("article_ids.pkl", "wb") as f:
    pickle.dump(article_ids, f)

print("Index and IDs saved.")


# Search function
def search(term, n):
    term_embedding = model.encode([term], convert_to_numpy=True, show_progress_bar=False).astype(np.float32)
    D, I = index.search(term_embedding, n)
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        results = []
        for idx, dist in zip(I[0], D[0]):
            article_id = article_ids[idx]
            cursor.execute("SELECT doc_full_name FROM article WHERE article_id = ?", (article_id,))
            doc_full_name = cursor.fetchone()[0]
            results.append({"article_id": article_id, "doc_full_name": doc_full_name, "distance": float(dist)})
    return results


# Test
if __name__ == "__main__":
    query = "Coding for Eventual Consistency"
    print(f"Searching for: {query}")
    for result in search(query, 10):
        print(f"ID: {result['article_id']}, Title: {result['doc_full_name']}, Distance: {result['distance']:.4f}")
