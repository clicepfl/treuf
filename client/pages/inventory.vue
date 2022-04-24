<template>
  <div class="m-40">
    <div class="text-center mb-20">
      Ceci est un texte explicatif de l'inventaire affiché ci-dessous
    </div>
    <div>
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