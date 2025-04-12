<script lang="ts">
  import { invoke } from "@tauri-apps/api/core";
  import { goto } from "$app/navigation";
  import SearchIcon from "$lib/components/SearchIcon.svelte";

  // Search term that binds to the input
  let searchTerm = "";

  // Article results
  type ArticleInfo = {
    id: number;
    name: string;
    description: string;
  };

  // Return type of the search_articles command
  type SearchArticleResult = {
    name: string;
    description: string;
  };

  let searchResults: ArticleInfo[] = [];
  let isSearching = false;
  let hasSearched = false;

  // Function to search articles
  async function searchArticles() {
    if (!searchTerm.trim()) return;

    isSearching = true;
    hasSearched = true;

    try {
      // Call the search_articles command with n=10
      const articleIds: number[] = await invoke("search_articles", {
        searchTerm,
        numResults: 10,
      });

      // Get article info for each id
      searchResults = await Promise.all(
        articleIds.map(async (id) => {
          const article_info: SearchArticleResult = await invoke(
            "get_article_info",
            {
              articleId: id,
            },
          );
          return {
            id,
            name: article_info.name,
            description: article_info.description,
          };
        }),
      );
    } catch (error) {
      console.error("Search error:", error);
    } finally {
      isSearching = false;
    }
  }

  // Function to goto an article page
  function gotoArticle(id: number) {
    goto(`/article/${id}`, { noScroll: true });
  }
</script>

<div class="container">
  <div class="search-container">
    <SearchIcon size={36} color="#243445" />
    <input
      type="text"
      class="search-input"
      bind:value={searchTerm}
      placeholder="Search..."
    />
    <button class="search-button" on:click={searchArticles}>
      {#if isSearching}Loading...{:else}Search{/if}
    </button>
  </div>

  {#if !hasSearched}
    <div class="welcome-container">
      <h1 class="welcome-title">Welcome to Article Search</h1>
      <p class="welcome-description">
        Enter a search term above to discover relevant articles
      </p>
    </div>
  {:else if searchResults.length === 0 && !isSearching}
    <div class="no-results">
      <h2>No results found</h2>
      <p>Try a different search term</p>
    </div>
  {:else}
    {#each searchResults as result}
      <div class="result-card">
        <h2 class="result-title">{result.name}</h2>
        <p class="result-description">{result.description}</p>
        <button class="read-button" on:click={() => gotoArticle(result.id)}
          >Read</button
        >
      </div>
    {/each}
  {/if}
</div>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400&display=swap");

  :global(*) {
    margin: 0;
    padding: 0;
    font-family: "Poppins", sans-serif;
    font-style: normal;
    font-weight: 400;
  }

  .container {
    padding: 64px 64px;
    width: auto;
    height: auto;
    background-color: #f0f4f8;
  }

  .search-container {
    background-color: #ffffff;
    border-radius: 30px;
    padding: 16px;
    margin: 0 64px 64px 64px; /* Extra 64px horizontal margin */
    display: flex;
    align-items: center;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
  }

  .search-input {
    flex-grow: 1;
    border: none;
    outline: none;
    font-size: 28px;
    padding: 10px;
  }

  .search-button {
    background-color: #243445;
    color: white;
    border: none;
    border-radius: 15px;
    padding: 12px 48px;
    font-size: 24px;
    font-weight: bold;
    cursor: pointer;
    transition-duration: 300ms;
  }

  .search-button:hover {
    transition-duration: 300ms;
    scale: 0.9;
    opacity: 0.8;
  }

  .result-card {
    background-color: #ffffff;
    border-radius: 30px;
    padding: 24px;
    margin-bottom: 40px; /* Space between items is 40px */
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
    display: flex;
    flex-direction: column;
  }

  .result-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 8px;
    color: black;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .result-description {
    font-size: 20px;
    color: black;
    margin-bottom: 32px;
    display: -webkit-box;
    overflow: hidden;
    flex-grow: 1;
  }

  .read-button {
    background-color: #243445;
    color: white;
    border: none;
    border-radius: 15px;
    padding: 12px 54px;
    font-size: 24px;
    font-weight: bold;
    cursor: pointer;
    display: inline-block;
    align-self: flex-start;
    transition-duration: 300ms;
  }

  .read-button:hover {
    transition-duration: 300ms;
    scale: 0.9;
    opacity: 0.8;
  }

  .welcome-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 50vh;
    color: #f0f4f8;
    text-align: center;
    padding: 24px;
  }

  .welcome-title {
    font-size: 48px;
    font-weight: bold;
    color: #243445;
    margin-bottom: 24px;
  }

  .welcome-description {
    font-size: 24px;
    color: #666;
    max-width: 600px;
  }

  .no-results {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 30vh;
    text-align: center;
    padding: 24px;
  }

  .no-results h2 {
    font-size: 32px;
    font-weight: bold;
    color: #243445;
    margin-bottom: 16px;
  }

  .no-results p {
    font-size: 20px;
    color: #666;
  }
</style>
