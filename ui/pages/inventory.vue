<template>
  <div>
    <div class="p-40 bg-gray-200">
      <p class="pb-8">CLICInventaire</p>
      <div class="p-4">
        <table class="table-auto rounded-xl bg-gray-300">
          <thead>
            <tr>
              <th class="text-left pl-8 pr-8 pb-3 border-gray-400" v-for="(header, i) in headers" :key="i">
                {{ header }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, i) in items" :key="i">
              <td
                class="p-4 pl-8 border-t-2 text-slate-400 border-gray-400"
                v-for="(field, j) in item" :key="j">
                {{ field }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import Vue from 'vue'

type Item = { quantity: number, borrowed: boolean }

export default Vue.extend({
  data: () => ({
    headers: ['Nom', 'Quantité', "Date d'emprunt"],
    items: [
      ['balai', 'un texte plutôt assez long', 'hier'],
      [4,5,6],
      [7,8,9]
    ]
  }),
  // asyncData: ({ $axios }) => {
  //   $axios.$get('localhost:5555/items')
  //   return {
  //     items: new Map<string, Item>()
  //   }
  // }
})
</script>