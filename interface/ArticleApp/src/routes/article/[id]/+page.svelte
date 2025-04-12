<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { invoke } from "@tauri-apps/api/core";
  import BackIcon from "$lib/components/BackIcon.svelte";

  export let data;
  let { id } = data;

  // Convert id to number
  const articleId = parseInt(id);

  // Article data
  let article = {
    name: "Loading...",
    description: "",
    body: "Loading article content...",
  };

  // Loading state
  let isLoading = true;

  // Recommended articles
  type ArticleInfo = {
    id: number;
    name: string;
  };

  // Return type of the search_articles command
  type SearchArticleResult = {
    name: string;
    description: string;
  };

  let recommendedArticles: ArticleInfo[] = [];

  // Load article data when component mounts
  onMount(async () => {
    try {
      // Get full article details
      article = await invoke("get_article_full", { articleId });

      // Get recommendations
      const recIds: number[] = await invoke("search_articles", {
        searchTerm: article.name + article.description,
        numResults: 10,
      });

      // Get info for each recommended article
      recommendedArticles = await Promise.all(
        recIds
          .filter((recId) => recId !== articleId) // Filter out current article
          .map(async (recId) => {
            const article_info: SearchArticleResult = await invoke(
              "get_article_info",
              {
                articleId: recId,
              },
            );
            return {
              id: recId,
              name: article_info.name,
            };
          }),
      );
    } catch (error) {
      console.error("Error loading article:", error);
    } finally {
      isLoading = false;
    }
  });

  // Function to go back to the previous page
  function goBack() {
    goto("/", { noScroll: true });
  }

  // Function to navigate to another article
  function gotoArticle(id: number) {
    goto(`/article/${id}`, { noScroll: true });
  }
</script>

<div class="page-container">
  <div class="article-scroll-container">
    <div class="article-container">
      <div class="article-title-area">
        <button class="back-button" on:click={goBack}>
          <BackIcon size={40} color="black"></BackIcon>
        </button>
        <h1 class="article-title">
          {article.name}
        </h1>
      </div>
      <div class="divider"></div>
      <div class="article-content">
        {#if isLoading}
          <p>Loading article content...</p>
        {:else}
          {article.body
            .replaceAll("\n\n", "DSDOCVLSJLD")
            .replaceAll("\n", " ")
            .replaceAll("DSDOCVLSJLD", "\n\n")}
        {/if}
      </div>
    </div>
  </div>
  <div class="sidebar-container">
    <div class="sidebar">
      <div class="sidebar-scroll-content">
        <h2 class="sidebar-title">More Like This</h2>
        {#if !isLoading}
          {#each recommendedArticles as recommendation}
            <div class="recommendation-card">
              <h3 class="recommendation-title">{recommendation.name}</h3>
              <button
                class="read-button"
                on:click={() => gotoArticle(recommendation.id)}>Read</button
              >
            </div>
          {/each}
        {/if}
      </div>
    </div>
  </div>
</div>

<style>
  .page-container {
    display: flex;
    width: 100%;
    height: 100vh;
    overflow: hidden;
  }

  .article-scroll-container {
    flex: 1;
    height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-width: none;
  }

  .article-container {
    padding: 64px 64px 64px 64px;
    min-height: 100%;
  }

  .article-title-area {
    display: flex;
    align-items: center;
    margin-bottom: 30px;
  }

  .article-title {
    font-size: 40px;
    font-weight: bold;
  }

  .back-button {
    background-color: transparent;
    border: none;
    cursor: pointer;
    margin-right: 16px;
  }

  .divider {
    height: 2px;
    background-color: #999999;
    margin-bottom: 64px;
  }

  .article-content {
    font-size: 20px;
    line-height: 1.6;
    white-space: pre-line;
  }

  .sidebar-container {
    width: 310px;
    height: 100vh;
    position: relative;
    flex-shrink: 0;
  }

  .sidebar {
    width: 230px;
    background-color: #243445;
    color: white;
    padding: 0px 40px;
    margin-top: 64px;
    border-top-left-radius: 30px;
    height: calc(100vh - 64px);
    display: flex;
    flex-direction: column;
  }

  .sidebar-title {
    font-size: 24px;
    font-weight: bold;
    margin-top: 40px;
    margin-bottom: 40px;
    text-align: center;
  }

  .sidebar-scroll-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-width: none;
  }

  .recommendation-card {
    background-color: white;
    border-radius: 30px;
    padding: 24px;
    margin-bottom: 32px;
    aspect-ratio: 1/1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .recommendation-title {
    font-size: 24px;
    font-weight: bold;
    color: black;
    margin-top: 0;
    margin-bottom: 24px;
  }

  .read-button {
    background-color: #243445;
    color: white;
    border: none;
    border-radius: 15px;
    padding: 12px 36px;
    font-size: 24px;
    font-weight: bold;
    cursor: pointer;
    display: block;
    width: 100%;
    text-align: center;
    transition-duration: 300ms;
  }

  .read-button:hover {
    transition-duration: 300ms;
    scale: 0.9;
    opacity: 0.8;
  }
</style>
