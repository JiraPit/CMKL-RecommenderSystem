import numpy as np
from sentence_transformers import SentenceTransformer
from usearch.index import Index
import sqlite3
from pathlib import Path

SENTENCE_EMBEDDING_MODEL = "all-MiniLM-L6-v2"

try:
    script_dir = Path(__file__).parent
except NameError:
    script_dir = Path.cwd()

DATA_DIR = (script_dir / "datasets" / "prepared").resolve()
USEARCH_INDEX_PATH = DATA_DIR / "usearch_index.usearch"
ARTICLE_DB_PATH = DATA_DIR / "article.db"

# Load embedding model and USearch index
model = SentenceTransformer(SENTENCE_EMBEDDING_MODEL, device="cpu")
usearch_index = Index.restore(str(USEARCH_INDEX_PATH))


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

    # Get the integer keys from matches
    integer_keys = [int(match.key) for match in matches]

    # Look up article IDs from the database
    conn = sqlite3.connect(ARTICLE_DB_PATH)
    cursor = conn.cursor()

    # Build placeholders for the IN clause
    placeholders = ",".join(["?" for _ in integer_keys])
    
    # Handle empty results case
    if not integer_keys:
        conn.close()
        return []
        
    # Fetch corresponding article_ids from the mapping table
    cursor.execute(
        f"SELECT text_article_id FROM usearch_id_map WHERE integer_key IN ({placeholders})",
        integer_keys,
    )
    
    results = cursor.fetchall()
    
    # Close the database connection
    conn.close()
    
    # Handle case where no mappings were found
    if not results:
        return []
        
    # Return the article IDs as integers (converted from text)
    try:
        # Try converting the text article IDs to integers
        return [int(row[0]) for row in results]
    except ValueError:
        # If conversion fails, return the original text article IDs
        # This is a fallback, but will likely cause issues with the proto definition
        print("WARNING: Could not convert article IDs to integers. Proto expects integers.")
        return [row[0] for row in results]
