<template>
  <div class="space-y-14">
    <div class="space-x-14 text-center">
      <button
        :class="available ? 'bg-red-600 hover:bg-red-500' : 'bg-blue-600 hover:bg-blue-500'"
        class="text-white font-medium px-4 py-2 rounded-md border"
        @click="showAvailable()"
      >
        Disponible
      </button>
      <button
        :class="borrowed ? 'bg-red-600 hover:bg-red-500' : 'bg-blue-600 hover:bg-blue-500'"
        class="text-white font-medium px-4 py-2 rounded-md border"
        @click="showBorrowed()"
      >
        Mon inventaire
      </button>
      <button
        :class="unavailable ? 'bg-red-600 hover:bg-red-500' : 'bg-blue-600 hover:bg-blue-500'"
        class="text-white font-medium px-4 py-2 rounded-md border"
        @click="showUnavailable()"
      >
        Emprunté
      </button>
    </div>
    <div v-show="available">
      <table class="table-fixed w-full shadow-md bg-blue-600 text-white font-medium">
        <thead>
          <tr class="hover:bg-blue-500">
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
            class="cursor-pointer hover:bg-blue-500"
            v-for="[id, item] in items" :key="id"
            @click="borrowItem(id)"
          >
            <td class="pl-8 pr-4 p-3 border-t border-white">
              {{ item.name }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-white">
              {{ quantities.get(id) }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-white">
              {{ item.a }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-white">
              {{ item.b }}
            </td>
            <td class="pl-4 pr-8 p-3 border-t border-white">
              {{ item.c }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-show="borrowed">
      <table class="table-fixed w-full shadow-md bg-blue-600 text-white font-medium">
        <thead>
          <tr class="hover:bg-blue-500">
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
            class="cursor-pointer hover:bg-blue-500"
            v-for="[id, item] in borrowedItems" :key="id"
            @click="unborrowItem(id)"
          >
            <td class="pl-8 pr-4 p-3 border-t border-white">
              {{ item.name }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-white">
              {{ borrowedQuantities.get(id) }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-white">
              {{ item.a }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-white">
              {{ item.b }}
            </td>
            <td class="pl-4 pr-8 p-3 border-t border-white">
              {{ item.c }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-show="unavailable">
      <table class="table-fixed w-full shadow-md bg-blue-600 text-white font-medium">
        <thead class="hover:bg-blue-500">
          <tr>
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
        <tbody class="hover:bg-blue-500">
          <tr
            v-for="[id, item] in unavailableItems" :key="id"
          >
            <td class="pl-8 pr-4 p-3 border-t border-white">
              {{ item.name }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-white">
              {{ unavailableQuantities.get(id) }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-white">
              {{ item.a }}
            </td>
            <td class="pl-4 pr-4 p-3 border-t border-white">
              {{ item.b }}
            </td>
            <td class="pl-4 pr-8 p-3 border-t border-white">
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

/**
 * This component should be split in smaller table subcomponents, which would
 * communicate via events. Everything is contained here until the API is set.
 */
export default {
  name: 'Inventory',
  data(): {
    headers: string[],
    items: Map<number, Item>,
    quantities: Map<number, number>
    borrowedItems: Map<number, Item>
    borrowedQuantities: Map<number, number>,
    unavailableItems: Map<number, Item>,
    unavailableQuantities: Map<number, number>,
    available: boolean,
    borrowed: boolean,
    unavailable: boolean
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
      borrowedQuantities: new Map([[0, 0], [1, 0], [2, 0]]),
      unavailableItems: new Map([
        [0, { id: 0, name: 'un balai beaucoup moins long', quantity: 12, a: 'a', b: 'b', c: 'c' }]
      ]),
      // is it needed? maybe the unavailable items simply change after POST
      unavailableQuantities: new Map([
        [0, 1]
      ]),
      available: true,
      borrowed: false,
      unavailable: false
    }
  },
  methods: {
    /**
     * Moves an item from available to borrowed
     * @param id The item ID
     */
    borrowItem(id: number): void {
      const item = this.items.get(id)
      const quantity = this.quantities.get(id)
      const borrowedQuantity = this.borrowedQuantities.get(id)
      if (item === undefined || quantity === undefined || borrowedQuantity === undefined) {
        return
      }

      this.quantities.set(id, quantity - 1)
      if (quantity <= 1) {
        this.items.delete(id)
      }
      if (!this.borrowedItems.has(id)) {
        this.borrowedItems.set(id, item)
      }
      this.borrowedQuantities.set(id, borrowedQuantity + 1)
    },
    /**
     * Moves an item from borrowed to available
     * @param id The item ID
     */
    unborrowItem(id: number): void {
      const borrowedItem = this.borrowedItems.get(id)
      const borrowedQuantity = this.borrowedQuantities.get(id)
      const quantity = this.quantities.get(id)
      if (borrowedItem === undefined || borrowedQuantity === undefined || quantity === undefined) {
        return
      }

      this.borrowedQuantities.set(id, borrowedQuantity - 1)
      if (borrowedQuantity <= 1) {
        this.borrowedItems.delete(id)
      }
      if (!this.items.has(id)) {
        this.items.set(id, borrowedItem)
      }
      this.quantities.set(id, quantity + 1)
    },
    /**
     * Moves the list of borrowed items to unavailable
     */
    confirmBorrowing(): void {

    },
    showAvailable(): void {
      this.borrowed = false
      this.unavailable = false
      this.available = true
    },
    showBorrowed(): void {
      this.available = false
      this.unavailable = false
      this.borrowed = true
    },
    showUnavailable(): void {
      this.available = false
      this.borrowed = false
      this.unavailable = true
    }
  }
}
</script>