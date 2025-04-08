import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle

# Load model and FAISS index
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
index = faiss.read_index("faiss_hnsw_index.bin")

# Search function
def search(term, n, article_ids):
    term_embedding = model.encode([term], convert_to_numpy=True, show_progress_bar=False).astype(np.float32)
    D, I = index.search(term_embedding, n)
    with sqlite3.connect("article.db") as conn:
        cursor = conn.cursor()
        results = []
        for idx, dist in zip(I[0], D[0]):
            article_id = article_ids[idx]
            cursor.execute("SELECT doc_full_name FROM article WHERE article_id = ?", (article_id,))
            doc_full_name = cursor.fetchone()[0]
            results.append({"article_id": article_id, "doc_full_name": doc_full_name, "distance": float(dist)})
    return results

if __name__ == '__main__':
    # Load article IDs
    article_ids = pickle.load(open('article_ids.pkl', 'rb'))

    query = "Coding for Eventual Consistency"
    print(f"Searching for: {query}")

    # Call search function with article_ids
    results = search(query, 10, article_ids)
    for result in results:
        print(f"ID: {result['article_id']}, Title: {result['doc_full_name']}, Distance: {result['distance']:.4f}")
