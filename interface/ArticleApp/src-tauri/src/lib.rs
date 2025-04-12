mod backend_interface;

use backend_interface::BackendInterface;
use tauri::State;
use tokio::sync::Mutex;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .manage(Mutex::new(AppState::default()))
        .invoke_handler(tauri::generate_handler![
            search_articles,
            get_article_info,
            get_article_full
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

//------------------------------[ APP STATE ]------------------------------

// Global state of the app
#[derive(Default)]
struct AppState {
    backend_interface: Option<BackendInterface>,
}

// Ensure the backend interface is initialized in the app state
async fn ensure_backend_interface_initialized(state: &mut AppState) -> Result<(), String> {
    if state.backend_interface.is_none() {
        state.backend_interface = Some(BackendInterface::new().await.map_err(|e| e.to_string())?);
    }
    Ok(())
}

//------------------------------[ Search Articles ]------------------------------

// Search for articles
#[tauri::command]
async fn search_articles(
    state: State<'_, Mutex<AppState>>,
    search_term: String,
    num_results: i32,
) -> Result<Vec<i32>, String> {
    let mut state_guard = state.lock().await;

    // Ensure the backend interface is initialized
    ensure_backend_interface_initialized(&mut state_guard).await?;

    // Perform search
    let result = state_guard
        .backend_interface
        .as_mut()
        .unwrap()
        .search(search_term, num_results)
        .await
        .map_err(|e| e.to_string())?;

    Ok(result.article_ids)
}

//------------------------------[ Get Article Info ]------------------------------

/// Article info structure
/// This is used as a return type for the `get_article_info` command
#[derive(serde::Serialize)]
pub struct ArticleInfo {
    pub name: String,
    pub description: String,
}

// Get article info
#[tauri::command]
async fn get_article_info(
    state: State<'_, Mutex<AppState>>,
    article_id: i32,
) -> Result<ArticleInfo, String> {
    let mut state_guard = state.lock().await;

    // Ensure the backend interface is initialized
    ensure_backend_interface_initialized(&mut state_guard).await?;

    // Get article info
    let result = state_guard
        .backend_interface
        .as_mut()
        .unwrap()
        .get_article_info(article_id)
        .await
        .map_err(|e| e.to_string())?;

    Ok(ArticleInfo {
        name: result.name,
        description: result.description,
    })
}

//------------------------------[ Get Article Full ]------------------------------

/// Full article structure
/// This is used as a return type for the `get_article_full` command
#[derive(serde::Serialize)]
pub struct ArticleFull {
    pub name: String,
    pub description: String,
    pub body: String,
}

// Get full article
#[tauri::command]
async fn get_article_full(
    state: State<'_, Mutex<AppState>>,
    article_id: i32,
) -> Result<ArticleFull, String> {
    let mut state_guard = state.lock().await;

    // Ensure the backend interface is initialized
    ensure_backend_interface_initialized(&mut state_guard).await?;

    // Get full article
    let result = state_guard
        .backend_interface
        .as_mut()
        .unwrap()
        .get_article_full(article_id)
        .await
        .map_err(|e| e.to_string())?;

    Ok(ArticleFull {
        name: result.name,
        description: result.description,
        body: result.body,
    })
}
