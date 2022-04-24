<template>
  <div class="mt-16 text-center">
    <div class="mb-20">
      <Login/>
    </div>
    <div>
      <NuxtLink to="/inventory">Inventaire</NuxtLink>
    </div>
  </div>
</template>

<script lang="ts">
import Login from '../components/Login.vue'

export default {
  name: 'IndexPage',
  components: {
    Login
  },
}
</script>