#[cfg(test)]
mod database_interface_test {
    use super::super::{get_article, get_article_info};
    use std::env;

    const TEST_ARTICLE_ID: i32 = 0;
    const TEST_ARTICLE_NAME: &str = "Detect Malfunctioning IoT Sensors with Streaming Analytics";
    const NON_EXISTENT_ARTICLE_ID: i32 = 9999999;

    #[test]
    fn test_get_article() {
        env::set_var("DB_PATH", "database/article.db");
        let article = get_article(TEST_ARTICLE_ID).unwrap();
        assert_eq!(article.doc_full_name, TEST_ARTICLE_NAME);
        assert!(!article.doc_body.is_empty());
    }

    #[test]
    fn test_get_article_info() {
        env::set_var("DB_PATH", "database/article.db");
        let articles = get_article_info(vec![TEST_ARTICLE_ID]).unwrap();
        assert_eq!(articles.len(), 1);
        assert_eq!(articles[0].doc_full_name, TEST_ARTICLE_NAME);
        assert!(!articles[0].doc_description.is_empty());
    }

    #[test]
    fn test_get_non_existent_article() {
        env::set_var("DB_PATH", "database/article.db");
        let result = get_article(NON_EXISTENT_ARTICLE_ID);
        assert!(result.is_err());
    }
}
