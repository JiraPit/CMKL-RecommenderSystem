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
  <path d="M15 18L9 12L15 6" stroke-linecap="round" stroke-linejoin="round" />
</svg>

<style>
  .search-icon {
    margin-right: 10px;
    margin-left: 10px;
  }
</style>
