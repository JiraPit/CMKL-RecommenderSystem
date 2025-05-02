import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from usearch.index import Index
from pathlib import Path

try:
    script_dir = Path(__file__).parent
except NameError:
    script_dir = Path.cwd()

DATA_DIR = (script_dir / "datasets" / "prepared").resolve()
ARTICLE_DB_PATH = DATA_DIR / "article.db"
OUTPUT_USEARCH_INDEX_PATH = DATA_DIR / "usearch_index.usearch"

model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

texts_to_embed = []
map_data_to_insert = []

with sqlite3.connect(ARTICLE_DB_PATH) as conn:
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usearch_id_map (
            integer_key INTEGER PRIMARY KEY,
            text_article_id TEXT NOT NULL
        )
    """
    )
    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_text_article_id ON usearch_id_map (text_article_id);
    """
    )

    print("Clearing previous ID map from database...")
    cursor.execute("DELETE FROM usearch_id_map")

    print("Fetching article data from database...")
    cursor.execute("SELECT article_id, doc_full_name, doc_description FROM articles")
    articles_data = cursor.fetchall()

    print("Preparing data and mapping...")
    for i, (text_article_id, name, desc) in enumerate(articles_data):
        combined_text = f"{name} {desc}"
        texts_to_embed.append(combined_text)
        map_data_to_insert.append((i, text_article_id))

    print(f"Inserting {len(map_data_to_insert)} mapping entries into database...")
    cursor.executemany(
        "INSERT INTO usearch_id_map (integer_key, text_article_id) VALUES (?, ?)",
        map_data_to_insert,
    )

    print("ID map table created and populated in the database.")


print(f"Generating embeddings for {len(texts_to_embed)} texts...")
embeddings = model.encode(
    texts_to_embed,
    convert_to_numpy=True,
    show_progress_bar=True,
).astype(np.float32)
embeddings = np.nan_to_num(embeddings)

print("Building USearch index...")
dimensions = embeddings.shape[1]
usearch_index = Index(ndim=dimensions, metric="cos", dtype="f32")

for i, embedding in enumerate(embeddings):
    integer_key = np.uint64(i)
    usearch_index.add(integer_key, embedding)

print(f"Saving USearch index to {OUTPUT_USEARCH_INDEX_PATH}...")
usearch_index.save(str(OUTPUT_USEARCH_INDEX_PATH))

print("Indexing complete. Index saved. ID map stored in database.")
