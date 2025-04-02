<script lang="ts">
  import { goto } from "$app/navigation";
  import SearchIcon from "$lib/components/SearchIcon.svelte";

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
    goto("/article/${id}", { noScroll: true });
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
    <button class="search-button"> Search </button>
  </div>

  {#each searchResults as result}
    <div class="result-card">
      <h2 class="result-title">{result.title}</h2>
      <p class="result-description">{result.description}</p>
      <button class="read-button" on:click={() => gotoArticle(22)}>Read</button>
    </div>
  {/each}
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
</style>
