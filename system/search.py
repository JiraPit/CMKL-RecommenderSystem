import numpy as np
from sentence_transformers import SentenceTransformer
from usearch.index import Index
import pickle
from pathlib import Path

SENTENCE_EMBEDDING_MODEL = "all-MiniLM-L6-v2"

USEARCH_INDEX_PATH = (
    Path(__file__).parent / "datasets" / "prepared" / "usearch_index.usearch"
).resolve()

ARTICLE_IDS_PATH = (
    Path(__file__).parent / "datasets" / "prepared" / "article_ids.pkl"
).resolve()


# Load embedding model, USearch index, and article IDs
model = SentenceTransformer(SENTENCE_EMBEDDING_MODEL, device="cpu")
article_ids = pickle.load(open(ARTICLE_IDS_PATH, "rb"))
usearch_index = Index.restore(USEARCH_INDEX_PATH)


# Search function
def search(term, n):
    # Embed the search term
    term_embedding = model.encode(
        [term],
        convert_to_numpy=True,
        show_progress_bar=False,
    ).astype(np.float32)

    # Use USearch to search for the nearest neighbors
    assert isinstance(usearch_index, Index)
    matches = usearch_index.search(term_embedding[0], count=n)

    # Map indices to article IDs
    result = [int(article_ids[int(match.key)]) for match in matches]
    return result
