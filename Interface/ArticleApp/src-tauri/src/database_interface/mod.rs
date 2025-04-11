mod test;
use std::env;

#[derive(serde::Serialize, serde::Deserialize)]
pub struct Article {
    pub doc_full_name: String,
    pub doc_body: String,
}

#[tauri::command]
/// Tauri command to get the name and body of an article by its ID
pub fn get_article(id: i32) -> Result<Article, String> {
    // Open the database connection
    let db_path = env::var("DB_PATH").map_err(|_| "DB_PATH environment variable not set")?;

    let conn = rusqlite::Connection::open(db_path)
        .map_err(|e| format!("Failed to open database connection: {}", e))?;

    // Retrieve the article from the database
    let mut stmt = conn
        .prepare("SELECT doc_full_name, doc_body FROM article WHERE article_id = ?1")
        .map_err(|e| format!("Failed to prepare SQL statement: {}", e))?;

    // Extract the article information
    let mut rows = stmt
        .query([id])
        .map_err(|e| format!("Failed to execute SQL query: {}", e))?;
    let article = rows
        .next()
        .map_err(|e| format!("Failed to retrieve article: {}", e))?;
    let article = match article {
        Some(article) => article,
        None => return Err("Article not found".to_string()),
    };

    Ok(Article {
        doc_full_name: article.get(0).unwrap_or("None".to_string()),
        doc_body: article.get(1).unwrap_or("None".to_string()),
    })
}

#[derive(serde::Serialize, serde::Deserialize)]
pub struct ArticleInfo {
    pub doc_full_name: String,
    pub doc_description: String,
}

#[tauri::command]
/// Tauri command to get the name and description of articles by their IDs
pub fn get_article_info(ids: Vec<i32>) -> Result<Vec<ArticleInfo>, String> {
    // Open the database connection
    let db_path = env::var("DB_PATH").map_err(|_| "DB_PATH environment variable not set")?;

    let conn = rusqlite::Connection::open(db_path)
        .map_err(|e| format!("Failed to open database connection: {}", e))?;

    // Retrieve the article from the database
    let mut stmt = conn
        .prepare("SELECT doc_full_name, doc_description FROM article WHERE article_id IN (?1)")
        .map_err(|e| format!("Failed to prepare SQL statement: {}", e))?;

    // Extract the article information
    let mut rows = stmt
        .query([ids
            .into_iter()
            .map(|id| id.to_string())
            .collect::<Vec<String>>()
            .join(",")])
        .map_err(|e| format!("Failed to execute SQL query: {}", e))?;
    let mut articles = Vec::new();
    while let Some(article) = rows
        .next()
        .map_err(|e| format!("Failed to retrieve article: {}", e))?
    {
        articles.push(ArticleInfo {
            doc_full_name: article.get(0).unwrap_or("None".to_string()),
            doc_description: article.get(1).unwrap_or("None".to_string()),
        });
    }

    Ok(articles)
}
