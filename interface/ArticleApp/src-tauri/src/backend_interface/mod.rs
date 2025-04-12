//
// This module defines an interface to interact with system backend via gRPC.
//

mod test;
pub mod system_backend {
    tonic::include_proto!("system_backend");
}

use anyhow::{Context, Result};
use system_backend::{
    recommender_service_client::RecommenderServiceClient, GetArticleFullRequest,
    GetArticleFullResponse, GetArticleInfoRequest, GetArticleInfoResponse, SearchRequest,
    SearchResponse,
};
use tonic::transport::Channel;

/// The interface to the system backend.
/// Only one instance of this struct should be created globally
/// to fully utilize the client stub.
pub struct BackendInterface {
    /// gRPC client for the system backend
    client: RecommenderServiceClient<Channel>,
}

impl BackendInterface {
    /// Creates a new instance of BackendInterface by connecting to the gRPC server
    pub async fn new() -> Result<Self> {
        // Create a channel and client that connects to the server
        let channel = Channel::from_static("http://0.0.0.0:6789")
            .connect()
            .await
            .context("Failed to connect to server")?;
        let client = RecommenderServiceClient::new(channel);

        Ok(Self { client })
    }

    /// Searches for articles based on a search term and number of results
    pub async fn search(
        &mut self,
        search_term: String,
        num_results: i32,
    ) -> Result<SearchResponse> {
        let request = SearchRequest {
            search_term,
            num_results,
        };

        let response = self
            .client
            .search(request)
            .await
            .context("Failed to search for articles")?;

        Ok(response.into_inner())
    }

    /// Gets basic information about an article (name and description)
    pub async fn get_article_info(&mut self, article_id: i32) -> Result<GetArticleInfoResponse> {
        let request = GetArticleInfoRequest { article_id };

        let response = self
            .client
            .get_article_info(request)
            .await
            .context("Failed to get article info")?;

        Ok(response.into_inner())
    }

    /// Gets full information about an article (name, description, and body)
    pub async fn get_article_full(&mut self, article_id: i32) -> Result<GetArticleFullResponse> {
        let request = GetArticleFullRequest { article_id };

        let response = self
            .client
            .get_article_full(request)
            .await
            .context("Failed to get full article")?;

        Ok(response.into_inner())
    }
}
