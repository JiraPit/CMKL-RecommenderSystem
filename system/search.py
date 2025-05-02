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

model = SentenceTransformer(SENTENCE_EMBEDDING_MODEL, device="cpu")
usearch_index = Index.restore(str(USEARCH_INDEX_PATH))


def search(term, n):
    term_embedding = model.encode(
        [term],
        convert_to_numpy=True,
        show_progress_bar=False,
    ).astype(np.float32)

    assert isinstance(usearch_index, Index)
    matches = usearch_index.search(term_embedding[0], count=n)

    integer_keys = [int(match.key) for match in matches]

    conn = sqlite3.connect(ARTICLE_DB_PATH)
    cursor = conn.cursor()

    placeholders = ",".join(["?" for _ in integer_keys])

    if not integer_keys:
        conn.close()
        return []
    cursor.execute(
        f"SELECT text_article_id FROM usearch_id_map WHERE integer_key IN ({placeholders})",
        integer_keys,
    )

    results = cursor.fetchall()
    conn.close()

    if not results:
        return []

    try:
        return [int(row[0]) for row in results]
    except ValueError:
        print(
            "WARNING: Could not convert article IDs to integers. Proto expects integers."
        )
        return [row[0] for row in results]
