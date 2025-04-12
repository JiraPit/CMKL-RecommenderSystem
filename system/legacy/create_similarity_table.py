import sqlite3
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
data_file = "articles_community.csv"
df = pd.read_csv(data_file)

# Rename 'Unnamed: 0' column if necessary
df.rename(columns={"Unnamed: 0": "id"}, inplace=True)

# Fill NaN values to avoid errors
df["doc_full_name"] = df["doc_full_name"].fillna("")
df["doc_description"] = df["doc_description"].fillna("")

# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings separately
full_name_embeddings = model.encode(df["doc_full_name"].tolist())
description_embeddings = model.encode(df["doc_description"].tolist())

# Concatenate embeddings for each document
combined_embeddings = np.hstack(
    (full_name_embeddings, description_embeddings)
)  # Horizontally stack

# Compute cosine similarity on concatenated embeddings
similarities = cosine_similarity(combined_embeddings)

# Find top 10 most similar articles for each article
top_ten_ids = []
for i in range(similarities.shape[0]):
    similar_indices = np.argsort(similarities[i])[::-1][1:11]  # Exclude itself
    top_ten = df.iloc[similar_indices]["article_id"].astype(str).tolist()
    top_ten_ids.append(top_ten)

# Connect to SQLite database (it will create the file if it doesn't exist)
db_name = "article_similarity.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create the table
create_table_sql = """
CREATE TABLE IF NOT EXISTS article_similarity (
    article_id TEXT PRIMARY KEY,
    top_1 TEXT, top_2 TEXT, top_3 TEXT, top_4 TEXT, top_5 TEXT,
    top_6 TEXT, top_7 TEXT, top_8 TEXT, top_9 TEXT, top_10 TEXT
);
"""
cursor.execute(create_table_sql)

# Insert data into the table
for idx, row in df.iterrows():
    article_id = row["article_id"]
    top_similar = top_ten_ids[idx]

    # Format values for SQL insertion
    values = [article_id] + top_similar
    insert_sql = f"""
    INSERT OR REPLACE INTO article_similarity 
    (article_id, top_1, top_2, top_3, top_4, top_5, top_6, top_7, top_8, top_9, top_10)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    cursor.execute(insert_sql, values)

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"SQLite database '{db_name}' has been created and data inserted successfully.")
