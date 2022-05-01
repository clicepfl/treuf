<template>
  <button class="
    rounded-full
    h-10 w-10
    text-white
    bg-blue-600
    hover:bg-white
    hover:text-blue-600
    hover:outline
    hover:outline-2
    hover:outline-blue-600"
  >
    <slot />
  </button>
</template>

<script lang="ts">
export default {
  name: 'PlusButton'
}
</script>