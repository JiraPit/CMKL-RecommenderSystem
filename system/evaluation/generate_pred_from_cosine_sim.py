import pandas as pd
import csv
from tqdm import tqdm
import sys
import os

dir_abs_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(dir_abs_path))
from search import search

# check cli argument
if len(sys.argv) != 3:
    print(f"{__file__} <input> <output>")
    sys.exit(1)
if not os.path.exists(sys.argv[1]):
    print(f"file {sys.argv[1]} not found")
    sys.exit(1)

# Define paths
input_csv = sys.argv[1]
output_file = sys.argv[2]

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Load article data
print(f"Loading article data from {input_csv}...")
articles_df = pd.read_csv(input_csv)

# Create output CSV file
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    # Write header row
    header = ["source_article"] + [f"top_{i+1}" for i in range(20)]
    writer.writerow(header)

    # For each article, find similar articles using vector search
    print(f"Generating vector similarity data for {len(articles_df)} articles...")
    skipped_count = 0

    for index, article in tqdm(articles_df.iterrows()):
        article_id = article.get(
            "article_id", index + 1
        )  # Use actual article_id if available

        # Skip articles with missing name or description
        if pd.isna(article["doc_full_name"]) or pd.isna(article["doc_description"]):
            print(f"Skipping article {article_id} due to missing name or description")
            skipped_count += 1
            continue

        name = article["doc_full_name"]
        description = article["doc_description"]

        # Concatenate name and description for vectorization
        article_text = f"{name} {description}"

        try:
            # Get top 21 similar articles (first will be self-match)
            similar_articles = search(article_text, 21)

            # Remove the first result (self-match) and take only the next 20
            # Make sure we have enough results
            if len(similar_articles) > 1:
                similar_articles = similar_articles[1:21]
            else:
                # If we don't have enough results, pad with empty strings
                similar_articles = similar_articles[1:] + [""] * (
                    20 - len(similar_articles) + 1
                )

            # Write results to CSV - using article_id for all columns
            row = [article_id] + similar_articles
            writer.writerow(row)
        except Exception as e:
            print(f"Error processing article {article_id}: {e}")
            skipped_count += 1

    print(f"Total articles skipped: {skipped_count}")

print(f"Vector similarity data saved to {output_file}")
