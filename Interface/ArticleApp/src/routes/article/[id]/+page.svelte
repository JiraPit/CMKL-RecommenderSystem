<script>
  import FadeHover from "../../../lib/components/FadeHover.svelte";
  import BackIcon from "./BackIcon.svelte";

  // Dummy article data
  const article = {
    title: "Super Fast String Matching in Python",
    content: `Traditional approaches to string matching such as the Jaro-Winkler or Levenshtein distance measure are too slow for large datasets. Using TF-IDF with N-Grams as 
terms to find similar strings transforms the problem into a matrix multiplication problem, which is computationally much cheaper. Using this approach made it possible to search for near duplicates in a set of 663,000 company names in 42 minutes using only a dual-core laptop.

NAME MATCHING
A problem that I have witnessed working with databases, and I think many other 
people with me, is name matching. Databases often have multiple entries that 
relate to the same entity, for example a person or company, where one entry has 
a slightly different spelling then the other. This is a problem, and you want to de-duplicate these. A similar problem occurs when you want to merge or join databases using the names as identifier.

Traditional approaches to string matching such as the Jaro-Winkler or Levenshtein distance measure are too slow for large datasets. Using TF-IDF with N-Grams as 
terms to find similar strings transforms the problem into a matrix multiplication problem, which is computationally much cheaper. Using this approach made it possible to search for near duplicates in a set of 663,000 company names in 42 minutes using only a dual-core laptop.

NAME MATCHING
A problem that I have witnessed working with databases, and I think many other 
people with me, is name matching. Databases often have multiple entries that 
relate to the same entity, for example a person or company, where one entry has 
a slightly different spelling then the other. This is a problem, and you want to de-duplicate these. A similar problem occurs when you want to merge or join databases using the names as identifier.

Traditional approaches to string matching such as the Jaro-Winkler or Levenshtein distance measure are too slow for large datasets. Using TF-IDF with N-Grams as 
terms to find similar strings transforms the problem into a matrix multiplication problem, which is computationally much cheaper. Using this approach made it possible to search for near duplicates in a set of 663,000 company names in 42 minutes using only a dual-core laptop.

NAME MATCHING
A problem that I have witnessed working with databases, and I think many other 
people with me, is name matching. Databases often have multiple entries that 
relate to the same entity, for example a person or company, where one entry has 
a slightly different spelling then the other. This is a problem, and you want to de-duplicate these. A similar problem occurs when you want to merge or join databases using the names as identifier.
`,
  };

  // Dummy recommended articles
  const recommendedArticles = [
    {
      id: "456",
      title: "Identify Useful HTTP API Tools",
    },
    {
      id: "789",
      title: "Identify Useful HTTP API Tools",
    },
    {
      id: "101",
      title: "Identify Useful HTTP API Tools",
    },
  ];

  function goBack() {
    window.history.back();
  }
</script>

<div class="page-container">
  <div class="article-scroll-container">
    <div class="article-container">
      <div class="article-title-area">
        <FadeHover>
          <button class="back-button" on:click={goBack}>
            <BackIcon size={40} color="black"></BackIcon>
          </button>
        </FadeHover>
        <h1 class="article-title">
          {article.title}
        </h1>
      </div>
      <div class="divider"></div>
      <div class="article-content">
        {article.content
          .replaceAll("\n\n", "DSDOCVLSJLD")
          .replaceAll("\n", " ")
          .replaceAll("DSDOCVLSJLD", "\n\n")}
      </div>
    </div>
  </div>

  <div class="sidebar-container">
    <div class="sidebar">
      <div class="sidebar-scroll-content">
        <h2 class="sidebar-title">More Like This</h2>
        {#each recommendedArticles as recommendation}
          <div class="recommendation-card">
            <h3 class="recommendation-title">{recommendation.title}</h3>
            <FadeHover>
              <button class="read-button">Read</button>
            </FadeHover>
          </div>
        {/each}
      </div>
    </div>
  </div>
</div>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap");

  :global(body) {
    margin: 0;
    padding: 0;
    font-family: "Poppins", sans-serif;
    overflow: hidden;
    height: 100vh;
  }

  :global(*) {
    scrollbar-width: none;
    -ms-overflow-style: none;
  }

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
    position: sticky;
    top: 0;
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
    padding-right: 10px;
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
    font-family: "Poppins", sans-serif;
    cursor: pointer;
    display: block;
    width: 100%;
    text-align: center;
  }
</style>
