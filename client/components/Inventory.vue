<template>
  <div class="space-y-14">
    <div class="space-x-14 text-center">
      <button
        :class="available ? 'text-blue-600 bg-white outline outline-2 outline-blue-600' : 'text-white bg-blue-600 hover:bg-blue-500'"
        class="font-medium px-4 py-2 rounded-md w-40"
        @click="showAvailable()"
      >
        Disponible
      </button>
      <button
        :class="borrowed ? 'text-blue-600 bg-white outline outline-2 outline-blue-600' : 'text-white bg-blue-600 hover:bg-blue-500'"
        class="font-medium px-4 py-2 rounded-md w-40"
        @click="showBorrowed()"
      >
        Mon inventaire
      </button>
      <button
        :class="unavailable ? 'text-blue-600 bg-white outline outline-2 outline-blue-600' : 'text-white bg-blue-600 hover:bg-blue-500'"
        class="font-medium px-4 py-2 rounded-md w-40"
        @click="showUnavailable()"
      >
        Emprunté
      </button>
    </div>
    <div v-show="available">
      <table class="table-fixed w-full bg-blue-600 text-white font-medium">
        <thead>
          <tr>
            <th class="bg-white w-16" />
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
          </tr>
        </thead>
        <tbody>
          <tr
            class="hover:bg-white hover:text-blue-600"
            v-for="[id, item] in items" :key="id"
          >
            <td class="text-left bg-white">
              <RoundButton @click="borrowItem(id)">
                +
              </RoundButton>
            </td>
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
          </tr>
        </tbody>
      </table>
    </div>
    <div v-show="borrowed">
      <table class="table-fixed w-full bg-blue-600 text-white font-medium">
        <thead>
          <tr>
            <th class="bg-white w-16" />
            <th class="text-left pl-8 pr-4 py-3">
              {{ borrowedHeaders[0] }}
            </th>
            <th class="text-left px-4 py-3">
              {{ borrowedHeaders[1] }}
            </th>
            <th class="text-left px-4 py-3">
              {{ borrowedHeaders[2] }}
            </th>
            <th class="text-left px-4 py-3">
              {{ borrowedHeaders[3] }}
            </th>
            <th class="text-left pl-4 pr-8 py-3">
              {{ borrowedHeaders[4] }}
            </th>
            <th class="bg-white w-40" />
          </tr>
        </thead>
        <tbody>
          <tr
            class="hover:bg-white hover:text-blue-600"
            v-for="[id, item] in borrowedItems" :key="id"
          >
            <td class="text-left bg-white">
              <RoundButton @click="unborrowItem(id)">
                -
              </RoundButton>
            </td>
            <td class="pl-8 pr-4 py-3 border-t border-white">
              {{ item.name }}
            </td>
            <td class="px-4 py-3 border-t border-white">
              {{ borrowedQuantities.get(id) }}
            </td>
            <td class="px-4 py-3 border-t border-white">
              {{ item.unit }}
            </td>
            <td class="px-4 py-3 border-t border-white">
              {{ item.state }}
            </td>
            <td class="pl-4 pr-8 py-3 border-t border-white">
              <Form>
                <Field name="date" :rules="isRequired">
                  
                </Field>
              </Form>
            </td>
            <td class="text-center bg-white">
              <button
                :class="borrowedDates.has(id) ? 'cursor-pointer' : 'cursor-not-allowed'"
                class="
                  font-medium text-white
                  bg-blue-600
                  rounded-md
                  px-4
                  py-2
                  hover:text-blue-600
                  hover:bg-white
                  hover:outline
                  hover:outline-2
                  hover:outline-blue-600"
                @click="confirmBorrowing(id)"
              >
                Emprunter
              </button>
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
            <th class="text-left px-4 py-3">
              {{ unavailableHeaders[4] }}
            </th>
            <th class="text-left pl-4 pr-8 py-3">
              {{ unavailableHeaders[5] }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            class="hover:bg-white hover:text-blue-600"
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
            <td class="px-4 py-3 border-t border-white">
              {{ item.by }}
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
import { Form, Field } from 'vee-validate'
import RoundButton from './RoundButton.vue'

interface Item {
  id: number
  name: string
  quantity: number
  unit: string,
  state: string
}

interface UnavailableItem extends Item {
  by: string
  date: Date
}

/**
 * This component should be split in smaller table subcomponents, which would
 * communicate via events. Everything is contained here until the API is set.
 */
export default {
  name: 'Inventory',
  components: {
    Form,
    Field,
    RoundButton
  },
  data(): {
    headers: string[],
    borrowedHeaders: string[],
    unavailableHeaders: string[],
    items: Map<number, Item>,
    quantities: Map<number, number>
    borrowedItems: Map<number, Item>
    borrowedQuantities: Map<number, number>,
    borrowedDates: Map<number, Date>,
    unavailableItems: Map<number, UnavailableItem>,
    unavailableQuantities: Map<number, number>,
    available: boolean,
    borrowed: boolean,
    borrow: boolean,
    unavailable: boolean
  } {
    return {
      headers: ['Nom', 'Quantité', 'Unité', 'État'],
      borrowedHeaders: ['Nom', 'Quantité', 'Unité', 'État', 'Emprunter le'],
      unavailableHeaders: ['Nom', 'Quantité', 'Unité', 'État', 'Emprunté par', 'Retour'],
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
      borrowedDates: new Map(),
      unavailableItems: new Map([
        [0, { id: 0,
              name: 'un balai beaucoup moins long',
              quantity: 12,
              unit: 'a',
              state: 'b',
              by: 'vous',
              date: new Date(2022, 3, 1, 14)
            }]
      ]),
      // is it needed? maybe the unavailable items simply change after POST
      unavailableQuantities: new Map([
        [0, 1]
      ]),
      available: true,
      borrowed: false,
      borrow: false,
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
    confirmBorrowing(id: number): void {
      const date = this.borrowedDates.get(id)
      if (date === undefined) {
        return
      }
      // POST request for item id
      this.borrowedItems.delete(id)
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
    isRequired(value: unknown) {
      if (value !== undefined && value instanceof Date) {
        return true
      }
      return 'This field is required'
    },
    prettyDate(date: Date): string {
      const zeroPad = (arg: number) => String(arg).padStart(2, '0')
      const day = zeroPad(date.getDate())
      const month = zeroPad(date.getMonth() + 1)
      const hours = zeroPad(date.getHours())

      const now = new Date(Date.now())
      const daysDiff = (date.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)
      if (daysDiff < 0) {
        return 'Déjà rendu'
      }
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