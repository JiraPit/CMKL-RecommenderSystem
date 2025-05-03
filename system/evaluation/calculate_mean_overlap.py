import pandas as pd
import sys
import os

# check cli argument
if len(sys.argv) != 2:
    print(f"{__file__} <input>")
    sys.exit(1)
elif not os.path.exists(sys.argv[1]):
    print("file doesn't exist")
    sys.exit(1)

# Read the CSV file
df = pd.read_csv(sys.argv[1])

# Calculate the mean of overlap_count_top20 column
mean_overlap = df['overlap_count_top20'].mean()

# Print the result
print(f"Mean of overlap_count_top20: {mean_overlap:.4f}")