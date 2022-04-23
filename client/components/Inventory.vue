<template>
  <div>
    <table class="table-auto w-full rounded-lg bg-blue-100">
      <thead>
        <tr class="hover:bg-blue-300">
          <th class="text-left pl-8 pr-4 p-3">
            {{ headers[0] }}
          </th>
          <th class="text-left pl-4 pr-4 p-3">
            {{ headers[1] }}
          </th>
          <th class="text-left pl-4 pr-8 p-3">
            {{ headers[2] }}
          </th>
        </tr>
      </thead>
      <tbody class="overflow-y-scroll" style="height: 50vh;">
        <tr v-for="(item, i) in items" :key="i" class="hover:bg-blue-300">
          <td class="p-3 pl-8 pr-4 border-t border-black">
            {{ item[0] }}
          </td>
          <td class="p-3 pl-4 pr-4 border-t border-black">
            {{ item[1] }}
          </td>
          <td class="p-3 pl-4 pr-8 border-t border-black">
            {{ item[2] }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'Inventory',
  data: () => ({
    headers: ['Nom', 'Quantité', "Date d'emprunt"],
    items: [
      ['balai', 'un texte plutôt assez long', 'hier'],
      [4,5,6],
      [7,8,9],
      [10,11,12],
      [10,11,12],
      [10,11,12],
      [10,11,12],
      [10,11,12],
      [10,11,12],
      [10,11,12],
      [10,11,12],
      [10,11,12],
      [10,11,12],
      [10,11,12],
    ]
  })
})
</script>