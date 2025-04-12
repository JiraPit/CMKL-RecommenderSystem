from search import search
import sqlite3
from pathlib import Path

ARTICLE_DB_PATH = (
    Path(__file__).parent / ".." / ".." / "Datasets" / "prepared" / "article.db"
).resolve()

if __name__ == "__main__":
    query = "Seven Databases in Seven Days"
    print(f"Searching for: {query}")

    # Call search function
    results = search(query, 5)

    # Fetch and print the results
    with sqlite3.connect(ARTICLE_DB_PATH) as conn:
        cursor = conn.cursor()
        for article_id in results:
            cursor.execute(
                "SELECT doc_full_name FROM article WHERE article_id = ?",
                (article_id,),
            )
            doc_full_name = cursor.fetchone()[0]
            print(f"ID: {article_id}, Title: {doc_full_name}")
