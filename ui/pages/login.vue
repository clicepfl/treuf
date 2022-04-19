<template>
  <div>
    <div class="center">
      <form accept-charset="UTF-8" @submit.prevent="onSubmit()" method="POST">
        <div>
          <label>Email address</label>
          <input
            type="input"
            v-model="email"
            class="form-control"
            placeholder="Email"
          />
        </div>
        <button v-if="success" type="submit">Se connecter</button>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { ValidationProvider, extend } from 'vee-validate'
import { required } from 'vee-validate/dist/rules'

export default Vue.extend({
  name: 'LoginPage',
  components: {
    ValidationProvider
  },
  data: () => ({
    username: '',
    email: '',
    message: '',
    success: false,
  }),
  methods: {
    // Submit the form input fields for login
    async onSubmit(): Promise<void> {
      let data = {
        email: this.email,
        username: this.username,
      }
      await this.$axios
        .$post('localhost:5000/login', data, {
          headers: {
            Accept: 'application/json',
          },
        })
        .then(
          (response: any) => {
            this.success = true
          },
          (error: any) => {
            
          }
        )
    },
  },
  mounted() {
    extend('password', {
      validate(value: string | number, { length }): boolean | string {
        if (typeof value === 'string') {
          return value.length >= length
        }
        return 'Your password must be longer than 4 characters'
      }
    })
  }
})
</script>