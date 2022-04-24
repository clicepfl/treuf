<template>
  <div class="space-y-8">
    <div v-show="borrowed">
      <table class="table-fixed w-full shadow-md border border-black bg-blue-100">
        <thead>
          <tr class="hover:bg-blue-300">
            <th class="text-left pl-8 pr-4 p-3">
              {{ headers[0] }}
            </th>
            <th class="text-left pl-4 pr-4 p-3">
              {{ headers[1] }}
            </th>
            <th class="text-left pl-4 pr-4 p-3">
              {{ headers[2] }}
            </th>
            <th class="text-left pl-4 pr-4 p-3">
              {{ headers[3] }}
            </th>
            <th class="text-left pl-4 pr-8 p-3">
              {{ headers[4] }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            class="cursor-pointer hover:bg-blue-300"
            v-for="[id, item] in borrowedItems" :key="id"
            @click="unborrowItem(id)"
          >
            <td class="pl-8 pr-4 p-3 border-t border-black">
              {{ item.name }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-black">
              {{ borrowedQuantities.get(id) }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-black">
              {{ item.a }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-black">
              {{ item.b }}
            </td>
            <td class="pl-4 pr-8 p-3 border-t border-black">
              {{ item.c }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-show="available">
      <table class="table-fixed w-full shadow-md border border-black bg-blue-100">
        <thead>
          <tr class="hover:bg-blue-300">
            <th class="text-left pl-8 pr-4 p-3">
              {{ headers[0] }}
            </th>
            <th class="text-left pl-4 pr-4 p-3">
              {{ headers[1] }}
            </th>
            <th class="text-left pl-4 pr-4 p-3">
              {{ headers[2] }}
            </th>
            <th class="text-left pl-4 pr-4 p-3">
              {{ headers[3] }}
            </th>
            <th class="text-left pl-4 pr-8 p-3">
              {{ headers[4] }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            class="cursor-pointer hover:bg-blue-300"
            v-for="[id, item] in items" :key="id"
            @click="borrowItem(id)"
          >
            <td class="pl-8 pr-4 p-3 border-t border-black">
              {{ item.name }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-black">
              {{ quantities.get(id) }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-black">
              {{ item.a }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-black">
              {{ item.b }}
            </td>
            <td class="pl-4 pr-8 p-3 border-t border-black">
              {{ item.c }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">

interface Item {
  id: number
  name: string
  quantity: number
  a: string,
  b: string,
  c: string
}

export default {
  name: 'Inventory',
  data(): {
    headers: string[],
    items: Map<number, Item>,
    quantities: Map<number, number>
    borrowedItems: Map<number, Item>
    borrowedQuantities: Map<number, number>
  } {
    return {
      headers: ['Nom', 'Quantité', 'A', 'B', 'C'],
      items: new Map([
        [0, { id: 0, name: 'un balai plutôt assez très long', quantity: 12, a: 'a', b: 'b', c: 'c' }],
        [1, { id: 1, name: 'aspirateur', quantity: 2, a: 'a', b: 'b', c: 'c' }],
        [2, { id: 2, name: 'marqueur', quantity: 47, a: 'a', b: 'b', c: 'c' }]
      ]),
      quantities: new Map([
        [0, 12],
        [1, 2],
        [2, 47]
      ]),
      borrowedItems: new Map(),
      borrowedQuantities: new Map([[0, 0], [1, 0], [2, 0]])
    }
  },
  computed: {
    available(): boolean {
      return this.items.size > 0
    },
    borrowed(): boolean {
      return this.borrowedItems.size > 0
    }
  },
  methods: {
    borrowItem(id: number): void {
      const item = this.items.get(id)
      const quantity = this.quantities.get(id)
      const borrowedQuantity = this.borrowedQuantities.get(id)
      if (item === undefined || quantity === undefined || borrowedQuantity === undefined) {
        return
      }
      console.log(item, quantity, borrowedQuantity)
      this.quantities.set(id, quantity - 1)
      if (quantity <= 1) {
        this.items.delete(id)
        this.quantities.delete(id)
      }
      this.borrowedItems.set(id, item)
      this.borrowedQuantities.set(id, borrowedQuantity + 1)
    },
    unborrowItem(id: number): void {

    },
    confirmBorrowing(): void {

    }
  }
}
</script>