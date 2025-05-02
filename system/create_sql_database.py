import csv
import sqlite3
import os


def create_article_database():
    # Define file paths
    input_csv = "datasets/original/articles/articles_community.csv"
    output_db = "datasets/prepared/article.db"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_db), exist_ok=True)

    # Connect to SQLite database
    conn = sqlite3.connect(output_db)
    cursor = conn.cursor()

    # Create table with article_id as primary key
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS articles (
        article_id TEXT PRIMARY KEY,
        doc_full_name TEXT,
        doc_description TEXT,
        doc_body TEXT
    )
    """
    )

    # Read CSV and insert data
    with open(input_csv, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        # Insert data row by row
        for row in csv_reader:
            cursor.execute(
                """
            INSERT OR REPLACE INTO articles (article_id, doc_full_name, doc_description, doc_body)
            VALUES (?, ?, ?, ?)
            """,
                (
                    row["article_id"],
                    row["doc_full_name"],
                    row["doc_description"],
                    row["doc_body"],
                ),
            )

    # Create index on article_id for faster lookups
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_article_id ON articles(article_id)")

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print(f"Database created successfully at {output_db}")


if __name__ == "__main__":
    create_article_database()
