import pandas as pd


def main():
    # Load the CSV files
    user_interactions = pd.read_csv("user_interaction_recommendations.csv")
    vector_similarity = pd.read_csv("vector_similarity_results.csv")

    # Convert to floats and then to integers (handling potential NaN values)
    user_interactions = user_interactions.astype(float).astype("Int64")
    vector_similarity = vector_similarity.astype(float).astype("Int64")
    
    # Determine the number of top columns in each dataset
    ui_top_columns = [col for col in user_interactions.columns if col.startswith("top_")]
    vs_top_columns = [col for col in vector_similarity.columns if col.startswith("top_")]
    max_top = min(len(ui_top_columns), len(vs_top_columns), 20)  # Cap at 20
    print(f"Working with {max_top} recommendation columns")

    # Create a dictionary for quick lookup of vector similarity recommendations
    vector_sim_dict = {}
    for _, row in vector_similarity.iterrows():
        source_id = row["source_article"]
        recommendations = set(
            row[f"top_{i}"] for i in range(1, max_top + 1) if f"top_{i}" in row.index and not pd.isna(row[f"top_{i}"])
        )
        vector_sim_dict[source_id] = recommendations

    # Results list
    results = []

    # Loop through each row in user interactions
    for _, row in user_interactions.iterrows():
        source_id = row["source_article"]

        # Skip if this source_id doesn't exist in vector_similarity
        if source_id not in vector_sim_dict:
            continue

        # Get user interaction recommendations for this source
        ui_recommendations = set(
            row[f"top_{i}"] for i in range(1, max_top + 1) if f"top_{i}" in row.index and not pd.isna(row[f"top_{i}"])
        )

        # Get vector similarity recommendations for this source
        vs_recommendations = vector_sim_dict[source_id]

        # Count the overlap
        overlap_count = len(ui_recommendations.intersection(vs_recommendations))

        # Add to results
        results.append({"source_article": source_id, "overlap_count": overlap_count})

    # Create and save results DataFrame
    results_df = pd.DataFrame(results)
    # Rename overlap_count to clarify it counts matches in top recommendations
    results_df = results_df.rename(columns={"overlap_count": f"overlap_count_top{max_top}"})
    results_df.to_csv("recommendation_comparison.csv", index=False)
    print(f"Comparison complete. Results saved to recommendation_comparison.csv")


if __name__ == "__main__":
    main()

