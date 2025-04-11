import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle

SENTENCE_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
FAISS_INDEX_PATH = "prepared/faiss_index.bin"
ARTICLE_IDS_PATH = "prepared/article_ids.pkl"


# Load embedding model, FAISS index, and article IDs
model = SentenceTransformer(SENTENCE_EMBEDDING_MODEL, device="cpu")
faiss_index = faiss.read_index(FAISS_INDEX_PATH)
article_ids = pickle.load(open(ARTICLE_IDS_PATH, "rb"))


# Search function
def search(term, n):
    # Embed the search term
    term_embedding = model.encode(
        [term],
        convert_to_numpy=True,
        show_progress_bar=False,
    ).astype(np.float32)

    # Use FAISS to search for the nearest neighbors
    _, indices = faiss_index.search(term_embedding, n)

    # Map indices to article IDs
    result = [article_ids[int(idx)] for idx in indices[0]]
    return result
