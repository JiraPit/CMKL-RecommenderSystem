<div class="fade-container">
  <slot></slot>
</div>

<style>
  .fade-container {
    transition: opacity 300ms ease;
    opacity: 1;
  }

  .fade-container:hover {
    transition: opacity 300ms ease;
    opacity: 0.7;
  }
</style>
