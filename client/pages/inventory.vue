<template>
  <div class="m-20 mt-10">
    <Inventory/>
  </div>
</template>

<script lang="ts">
import Inventory from '../components/Inventory.vue'

export default {
  name: 'InventoryPage',
  components: {
    Inventory
  },
}
</script>