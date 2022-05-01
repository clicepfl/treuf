<template>
  <div class="space-y-14">
    <div class="space-x-14 text-center">
      <button
        :class="available ? 'text-blue-600 bg-white outline outline-2 outline-blue-600' : 'text-white bg-blue-600 hover:bg-blue-500'"
        class="font-medium px-4 py-2 rounded-md"
        @click="showAvailable()"
      >
        Disponible
      </button>
      <button
        :class="borrowed ? 'text-blue-600 bg-white outline outline-2 outline-blue-600' : 'text-white bg-blue-600 hover:bg-blue-500'"
        class="font-medium px-4 py-2 rounded-md border"
        @click="showBorrowed()"
      >
        Mon inventaire
      </button>
      <button
        :class="unavailable ? 'text-blue-600 bg-white outline outline-2 outline-blue-600' : 'text-white bg-blue-600 hover:bg-blue-500'"
        class="font-medium px-4 py-2 rounded-md border"
        @click="showUnavailable()"
      >
        Emprunté
      </button>
    </div>
    <div v-show="available">
      <table class="table-fixed w-full bg-blue-600 text-white font-medium">
        <thead>
          <tr>
            <th class="text-left pl-8 pr-4 py-3">
              {{ headers[0] }}
            </th>
            <th class="text-left px-4 py-3">
              {{ headers[1] }}
            </th>
            <th class="text-left px-4 py-3">
              {{ headers[2] }}
            </th>
            <th class="text-left pl-4 pr-8 py-3">
              {{ headers[3] }}
            </th>
            <th class="bg-white w-20" />
          </tr>
        </thead>
        <tbody>
          <tr
            class="hover:bg-white hover:text-blue-600"
            v-for="[id, item] in items" :key="id"
          >
            <td class="pl-8 pr-4 py-3 border-t border-white">
              {{ item.name }}
            </td>
            <td class="px-4 py-3 border-t border-white">
              {{ quantities.get(id) }}
            </td>
            <td class="px-4 py-3 border-t border-white">
              {{ item.unit }}
            </td>
            <td class="pl-4 pr-8 py-3 border-t border-white">
              {{ item.state }}
            </td>
            <td class="text-right bg-white w-20">
              <RoundButton @click="borrowItem(id)">
                +
              </RoundButton>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-show="borrowed">
      <table class="table-fixed w-full bg-blue-600 text-white font-medium">
        <thead>
          <tr>
            <th class="text-left pl-8 pr-4 py-3">
              {{ headers[0] }}
            </th>
            <th class="text-left px-4 py-3">
              {{ headers[1] }}
            </th>
            <th class="text-left px-4 py-3">
              {{ headers[2] }}
            </th>
            <th class="text-left pl-4 pr-8 py-3">
              {{ headers[3] }}
            </th>
            <th class="bg-white w-20" />
          </tr>
        </thead>
        <tbody>
          <tr
            class="hover:bg-white hover:text-blue-600"
            v-for="[id, item] in borrowedItems" :key="id"
          >
            <td class="pl-8 pr-4 py-3 border-t border-white">
              {{ item.name }}
            </td>
            <td class="px-4 py-3 border-t border-white">
              {{ borrowedQuantities.get(id) }}
            </td>
            <td class="px-4 py-3 border-t border-white">
              {{ item.unit }}
            </td>
            <td class="pl-4 pr-8 py-3 border-t border-white">
              {{ item.state }}
            </td>
            <td class="text-right bg-white w-20">
              <RoundButton @click="unborrowItem(id)">
                -
              </RoundButton>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-show="unavailable">
      <table class="table-fixed w-full bg-blue-600 text-white font-medium">
        <thead>
          <tr>
            <th class="text-left pl-8 pr-4 py-3">
              {{ unavailableHeaders[0] }}
            </th>
            <th class="text-left px-4 py-3">
              {{ unavailableHeaders[1] }}
            </th>
            <th class="text-left px-4 py-3">
              {{ unavailableHeaders[2] }}
            </th>
            <th class="text-left px-4 py-3">
              {{ unavailableHeaders[3] }}
            </th>
            <th class="text-left pl-4 pr-8 py-3">
              {{ unavailableHeaders[4] }}
            </th>
          </tr>
        </thead>
        <tbody class="hover:bg-white hover:text-blue-600">
          <tr
            v-for="[id, item] in unavailableItems" :key="id"
          >
            <td class="pl-8 pr-4 py-3 border-t border-white">
              {{ item.name }}
            </td>
            <td class="px-4 py-3 border-t border-white">
              {{ unavailableQuantities.get(id) }}
            </td>
            <td class="px-4 py-3 border-t border-white">
              {{ item.unit }}
            </td>
            <td class="px-4 py-3 border-t border-white">
              {{ item.state }}
            </td>
            <td class="pl-4 pr-8 py-3 border-t border-white">
              {{ prettyDate(item.date) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">

import RoundButton from './RoundButton.vue'

interface Item {
  id: number
  name: string
  quantity: number
  unit: string,
  state: string
}

interface UnavailableItem extends Item {
  date: Date
}

/**
 * This component should be split in smaller table subcomponents, which would
 * communicate via events. Everything is contained here until the API is set.
 */
export default {
  name: 'Inventory',
  components: {
    RoundButton
  },
  data(): {
    headers: string[],
    items: Map<number, Item>,
    quantities: Map<number, number>
    borrowedItems: Map<number, Item>
    borrowedQuantities: Map<number, number>,
    unavailableHeaders: string[],
    unavailableItems: Map<number, UnavailableItem>,
    unavailableQuantities: Map<number, number>,
    available: boolean,
    borrowed: boolean,
    unavailable: boolean
  } {
    return {
      headers: ['Nom', 'Quantité', 'Unité', 'État'],
      items: new Map([
        [0, { id: 0, name: 'un balai plutôt assez très long', quantity: 12, unit: 'a', state: 'b'}],
        [1, { id: 1, name: 'aspirateur', quantity: 2, unit: 'a', state: 'b'}],
        [2, { id: 2, name: 'marqueur', quantity: 47, unit: 'a', state: 'b'}]
      ]),
      quantities: new Map([
        [0, 12],
        [1, 2],
        [2, 47]
      ]),
      borrowedItems: new Map(),
      borrowedQuantities: new Map([[0, 0], [1, 0], [2, 0]]),
      unavailableHeaders: ['Nom', 'Quantité', 'Unité', 'État', 'Retour'],
      unavailableItems: new Map([
        [0, { id: 0,
              name: 'un balai beaucoup moins long',
              quantity: 12,
              unit: 'a',
              state: 'b',
              date: new Date(2022, 4, 3, 14)
            }]
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
    },
    prettyDate(date: Date): string {
      const zeroPad = (arg: number) => String(arg).padStart(2, '0')
      const day = zeroPad(date.getDay())
      const month = zeroPad(date.getMonth() + 1)
      const hours = zeroPad(date.getHours())

      const now = new Date(Date.now())
      const daysDiff = Math.abs(now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24)
      let when: string
      if (daysDiff < 2) {
        when = date.getDay() === now.getDay() ? 'Aujourd\'hui' : 'Demain'
      } else {
        when = `${day}.${month}`
      }
      return when + ` à ${hours}h`
    }
  }
}
</script>