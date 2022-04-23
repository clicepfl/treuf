<template>
  <div>
    <div>
      <Login/>
    </div>
    <div>
      <NuxtLink to="/inventory">Inventaire</NuxtLink>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Login from '../components/Login.vue'

export default Vue.extend({
  name: 'IndexPage',
  components: {
    Login
  },
})
</script>