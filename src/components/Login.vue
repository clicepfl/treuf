<template>
  <div class="space-y-4">
    <div>
      <ValidationProvider rules="minmax:4,24|required" v-slot="{ errors }">
        <input v-model="username" type="text">
        <span>{{ errors[0] }}</span>
      </ValidationProvider>
    </div>
    <div>
      <ValidationProvider rules="minmax:8,32|required" v-slot="{ errors }">
        <input v-model="password" type="text">
        <span>{{ errors[0] }}</span>
      </ValidationProvider>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { ValidationProvider } from 'vee-validate'

export default Vue.extend({
  name: 'Login',
  components: {
    ValidationProvider
  },
  data: () => ({
    username: '',
    password: '',
    success: false,
  }),
  methods: {
    // Submit the form input fields for login
    async onSubmit(): Promise<void> {
      let data = {
        username: this.username,
        password: this.password
      }
      await this.$axios
        .$post('localhost:5000/login', data, {
          headers: {
            Accept: 'application/json',
          },
        })
        .then(
          (response: any) => { this.success = true },
          (error: any) => {}
        )
    },
  },
})
</script>