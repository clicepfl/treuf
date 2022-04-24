<template>
  <div class="m-40 mt-20">
    <div class="text-center">
      Ceci est un texte explicatif de l'inventaire affiché ci-dessous
    </div>
    <div class="mt-20">
      <Inventory/>
    </div>
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