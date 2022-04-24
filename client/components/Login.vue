<template>
  <div class="space-y-4">
    <div>Nom d'utilisateur</div>
    <div>Mot de passe</div>
    <!-- <div>
      <ValidationProvider rules="minmax:4,24|required" v-slot="{ errors }">
        <input v-model="username" type="text">
        <span>{{ errors[0] }}</span>
      </ValidationProvider>
    </div>
    <div class="ring-2">
      <ValidationProvider rules="minmax:8,32|required" v-slot="{ errors }">
        <input v-model="password" type="text">
        <span>{{ errors[0] }}</span>
      </ValidationProvider>
    </div> -->
  </div>
</template>

<script lang="ts">

export default {
  name: 'Login',
  components: {},
  data(): {
    username: string,
    password: string,
    success: boolean
  } {
    return {
      username: '',
      password: '',
      success: false
    }
  },
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
}
</script>