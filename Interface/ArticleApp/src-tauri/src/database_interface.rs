use std::env;

#[derive(serde::Serialize, serde::Deserialize)]
pub struct ReadableArticle {
    pub doc_full_name: String,
    pub doc_body: String,
}

#[tauri::command]
/// Tauri command to get the name and body of an article by its ID
pub fn get_article(id: i32) -> Result<ReadableArticle, String> {
    // Open the database connection
    let db_path = env::var("DB_PATH").map_err(|_| "DB_PATH environment variable not set")?;

    let conn = rusqlite::Connection::open(db_path)
        .map_err(|e| format!("Failed to open database connection: {}", e))?;

    // Retrieve the article from the database
    let mut stmt = conn
        .prepare("SELECT doc_full_name, doc_body FROM articles WHERE id = ?1")
        .map_err(|e| format!("Failed to prepare SQL statement: {}", e))?;
    let mut rows = stmt
        .query([id])
        .map_err(|e| format!("Failed to execute SQL query: {}", e))?;
    let article = rows
        .next()
        .map_err(|e| format!("Failed to retrieve article: {}", e))?
        .unwrap();

    Ok(ReadableArticle {
        doc_full_name: article.get(0).unwrap_or("None".to_string()),
        doc_body: article.get(1).unwrap_or("None".to_string()),
    })
}

#[derive(serde::Serialize, serde::Deserialize)]
pub struct SearchResult {
    pub entries: Vec<SearchResultEntry>,
}

#[derive(serde::Serialize, serde::Deserialize)]
pub struct SearchResultEntry {
    pub id: String,
    pub doc_full_name: String,
    pub doc_description: String,
}

#[tauri::command]
/// Tauri command to provide search results using TF-IDF
pub fn search(query: String) -> Result<SearchResult, String> {
    // Open the database connection
    let db_path = env::var("DB_PATH").unwrap();
    let conn = rusqlite::Connection::open(db_path).unwrap();

    Ok(SearchResult { entries: vec![] })
}
