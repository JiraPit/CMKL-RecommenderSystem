<script>
  export let size = 24;
  export let color = "currentColor";
  export let strokeWidth = 2;
</script>

<svg
  viewBox="0 0 24 24"
  width={size}
  height={size}
  stroke={color}
  fill="none"
  stroke-width={strokeWidth}
  stroke-linecap="round"
  class="search-icon"
>
  <circle cx="11" cy="11" r="8"></circle>
  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
</svg>

<style>
  .search-icon {
    margin-right: 15px;
    margin-left: 15px;
  }
</style>
