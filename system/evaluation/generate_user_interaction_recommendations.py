import pandas as pd
import csv
from collections import defaultdict
from tqdm import tqdm

# Load user-item interactions data
print("Loading user-item interactions data...")
interactions_df = pd.read_csv("datasets/original/articles/user-item-interactions.csv")

# Group by email to find what users read
print("Processing user interactions...")
user_articles = defaultdict(list)
for _, row in interactions_df.iterrows():
    email = row["email"]
    article_id = row["article_id"]
    user_articles[email].append(article_id)

# Create co-reading matrix to find what other articles were read by users who read each article
article_co_reads = defaultdict(lambda: defaultdict(int))
print("Building co-reading matrix...")
for email, articles in tqdm(user_articles.items()):
    # For each article the user read
    for i in range(len(articles)):
        article_id = articles[i]
        # Increment co-reading count with every other article the same user read
        for j in range(len(articles)):
            if i != j:  # Skip self-connections
                other_article = articles[j]
                article_co_reads[article_id][other_article] += 1

# For each article, find top 20 co-read articles
print("Finding top co-read articles...")
all_articles = interactions_df["article_id"].unique()
recommendations = {}

for article_id in tqdm(all_articles):
    # Get all co-read articles with counts
    co_read_counts = article_co_reads[article_id]

    # Sort by count (descending)
    sorted_co_reads = sorted(co_read_counts.items(), key=lambda x: x[1], reverse=True)

    # Take top 20 (or fewer if there aren't 20), excluding the source article itself
    top_20 = []
    for article, _ in sorted_co_reads:
        if article != article_id:  # Ensure an article doesn't recommend itself
            top_20.append(article)
            if len(top_20) == 20:  # Stop once we have 20 articles
                break

    # Pad with empty strings if fewer than 20
    while len(top_20) < 20:
        top_20.append("")

    recommendations[article_id] = top_20

# Write to CSV
output_file = "evaluation/user_interaction_recommendations.csv"
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)

    # Write header
    header = ["source_article"] + [f"top_{i+1}" for i in range(20)]
    writer.writerow(header)

    # Write recommendations for each article
    for article_id, recommended in recommendations.items():
        writer.writerow([article_id] + recommended)

print(f"User interaction recommendations saved to {output_file}")
