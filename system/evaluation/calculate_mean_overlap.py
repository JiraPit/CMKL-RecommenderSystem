import pandas as pd

# Read the CSV file
df = pd.read_csv('recommendation_comparison.csv')

# Calculate the mean of overlap_count_top20 column
mean_overlap = df['overlap_count_top20'].mean()

# Print the result
print(f"Mean of overlap_count_top20: {mean_overlap:.4f}")