#[cfg(test)]
mod backend_interface_test {
    use super::super::BackendInterface;

    async fn connect_to_service() -> BackendInterface {
        let channel = tonic::transport::Channel::from_shared("http://0.0.0.0:6789")
            .unwrap()
            .connect()
            .await
            .unwrap();

        let client =
            super::super::system_backend::recommender_service_client::RecommenderServiceClient::new(
                channel,
            );

        BackendInterface { client }
    }

    #[tokio::test]
    async fn search_test() {
        let mut client = connect_to_service().await;

        let response = client.search("database".to_string(), 2).await.unwrap();
        assert_eq!(response.article_ids.len(), 2);

        let response = client.search("seven days".to_string(), 3).await.unwrap();
        assert_eq!(response.article_ids.len(), 3);
    }

    #[tokio::test]
    async fn get_article_info_test() {
        let mut client = connect_to_service().await;

        let article_info = client.get_article_info(1).await.unwrap();
        assert_eq!(article_info.name.is_empty(), false);
        assert_eq!(article_info.description.is_empty(), false);

        let article_info = client.get_article_info(2).await.unwrap();
        assert_eq!(article_info.name.is_empty(), false);
        assert_eq!(article_info.description.is_empty(), false);

        let result = client.get_article_info(-1).await;
        assert!(result.is_err());
    }

    #[tokio::test]
    async fn get_article_full_test() {
        let mut client = connect_to_service().await;

        let article_full = client.get_article_full(1).await.unwrap();
        assert_eq!(article_full.name.is_empty(), false);
        assert_eq!(article_full.description.is_empty(), false);
        assert_eq!(article_full.body.is_empty(), false);

        let article_full = client.get_article_full(3).await.unwrap();
        assert_eq!(article_full.name.is_empty(), false);
        assert_eq!(article_full.description.is_empty(), false);
        assert_eq!(article_full.body.is_empty(), false);

        let result = client.get_article_full(-1).await;
        assert!(result.is_err());
    }
}
