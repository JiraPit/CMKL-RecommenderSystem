<script lang="ts">
  import SearchIcon from "./SearchIcon.svelte";
  import { goto } from "$app/navigation";
  import FadeHover from "../lib/components/FadeHover.svelte";

  // Dummy search term that binds to the input
  let searchTerm = "";

  // Dummy data mimicking backend results
  let searchResults = [
    {
      title: "Super Fast String Matching in Python",
      description:
        "Traditional approaches to string matching such as the Jaro-Winkler or Levenshtein distance measure are too slow for large datasets. Using TF-IDF with N-Grams",
    },
    {
      title: "On-demand backups with the Compose API and Node.js",
      description:
        "You need your latest backup and you need it automatically? We can show you how to create an on-demand backup and retrieve it automatically using the Compose API and Node.js.",
    },
    {
      title: "On-demand backups with the Compose API and Node.js",
      description:
        "You need your latest backup and you need it automatically? We can show you how to create an on-demand backup and retrieve it automatically using the Compose API and Node.js.",
    },
  ];

  // Function to goto an article page
  function gotoArticle(id: number) {
    goto(`/article/${id}`);
    return null;
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
    <FadeHover>
      <button class="search-button"> Search </button>
    </FadeHover>
  </div>

  {#each searchResults as result}
    <div class="result-card">
      <h2 class="result-title">{result.title}</h2>
      <p class="result-description">{result.description}</p>
      <FadeHover>
        <button class="read-button" on:click={gotoArticle(22)}>Read</button>
      </FadeHover>
    </div>
  {/each}
</div>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap");

  .container {
    font-family: "Poppins", sans-serif;
    max-width: 100%;
    margin: 0;
    padding: 64px 64px; /* Top/bottom 64px, left/right 64px */
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
    font-family: "Poppins", sans-serif;
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
    font-family: "Poppins", sans-serif;
    cursor: pointer;
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
    font-family: "Poppins", sans-serif;
    cursor: pointer;
    display: inline-block;
    align-self: flex-start;
  }
</style>
