<template>
  <div class="bg-black">
    <div class="m-40">
      <p class="pb-8">CLICInventaire</p>
      <div>
        <table class="table-auto border-collapse">
          <thead>
            <tr>
              <th class="border-b text-left pl-8 pb-3" v-for="(header, i) in headers" :key="i">
                {{ header }}
              </th>
            </tr>
          </thead>
          <tbody class="bg-slate-800">
            <tr v-for="(item, i) in items" :key="i">
              <td
                class="p-4 pl-8 border-b text-slate-500 border-slate-100"
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