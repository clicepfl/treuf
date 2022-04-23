<template>
  <div>
    <div class="m-40">
      <Inventory/>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Inventory from '../components/Inventory.vue'

export default Vue.extend({
  name: 'InventoryPage',
  components: {
    Inventory
  },
})
</script>