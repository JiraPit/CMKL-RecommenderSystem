import pandas as pd
import csv
import numpy as np
import sys
import os

# check cli argument
cli_arg_count = 3
if len(sys.argv) != cli_arg_count:
    print(f"{__file__} <input> <output>")
    sys.exit(1)
if not os.path.exists(sys.argv[1]):
    print(f"file {sys.argv[1]} not found")
    sys.exit(1)

# Load user-item interactions data
print("Loading user-item interactions data...")
interactions_df = pd.read_csv(sys.argv[1])

email_col = interactions_df["email"]
articles_col = interactions_df["article_id"]

# Used to map the indexs in the matrix back to the values
emails = email_col.unique()
articles = articles_col.unique()

# Creating the covariance matrix
print("Creating the covariance matrix...")
interaction_matrix = np.zeros((emails.shape[0], articles.shape[0]))
for i in email_col.index:
    email_idx = pd.Index(emails).get_loc(email_col.iloc[i])
    article_idx = pd.Index(articles).get_loc(articles_col.iloc[i])
    interaction_matrix[email_idx][article_idx] += 1

def calc_covar_matrix(A: np.ndarray):
    col_vec_norms = np.linalg.norm(A, axis=0)[np.newaxis]
    normalized_A = A / col_vec_norms
    return normalized_A.T @ normalized_A

covar_matrix = calc_covar_matrix(interaction_matrix)

# Ranking based on the covariance
print("Ranking based on the covariance...")
# Remove self-connections
diag_idxs = (np.identity(articles.shape[0]) == 1)
covar_matrix[diag_idxs] = 0
# Sort in descending order ([::-1] reverses the element order after the sort)
ranking_matrix = np.argsort(covar_matrix, axis=1)[:, ::-1]

get_articles = lambda a: list(np.apply_along_axis(lambda i: articles[i], 0, a))

recommendations = {id: get_articles(ranking[:20]) for id, ranking in zip(articles, ranking_matrix)}

# Write to CSV
output_file = sys.argv[2]
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)

    # Write header
    header = ["source_article"] + [f"top_{i+1}" for i in range(20)]
    writer.writerow(header)

    # Write recommendations for each article
    for article_id, recommended in recommendations.items():
        writer.writerow([article_id] + recommended)

print(f"User interaction recommendations saved to {output_file}")
