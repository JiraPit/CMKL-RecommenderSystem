use std::fs;

fn main() {
    // Copy dataset files to the dataset directory
    fs::copy(
        "../../../Datasets/prepared/article.db",
        "dataset/article.db",
    )
    .expect("Failed to copy article.db");

    tauri_build::build()
}
