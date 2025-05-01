import { defineStore } from 'pinia'
import type { FeedType } from '@/utils/types.ts'
import { getFeedBaseUrl } from '@/utils/helpers.ts'

interface Attachment {
  url: string;
  type: 'audio' | 'video' | 'embed'
}

interface FeedItem {
  attachments: Attachment[]
  description: string
  has_paid_content: boolean
  link: string
  preview: string
  pub_date: string
  title: string
  feed: number
  actions: string[]
  id: number
}

type Filter = string | string[]
type NullableFilter = Filter | null
type FilterRecord = Record<string, Filter>

interface FeedState {
  items: FeedItem[]
  total: number
  filters: Record<'default' | string, FilterRecord>
  isLoading: boolean,
  type: FeedType,
  url: string,
}

export const useFeedStore = defineStore('feed', {
  state: () =>
    ({
      items: [],
      total: 0,
      isLoading: false,
      type: 'generic',
      url: getFeedBaseUrl('generic'),
      filters: {
        default: { exclude: ['viewed', 'not_interesting'] },
        favorites: { exclude: ['not_interesting'] },
        favorites_detail: { exclude: ['not_interesting'] }
      }
    }) as FeedState,
  getters: {
    getItemById: (state: FeedState) => (id: number) => state.items.find((item) => item.id === id),
    getFilters: (state: FeedState) => (category: string) => {
      if (!state.filters[category]) {
        return state.filters.default
      }

      return state.filters[category]
    },
    isEmpty: (state: FeedState) => state.items.length === 0
  },
  actions: {
    setItems(items: FeedItem[]) {
      this.items = items
    },
    setFilters(category: string, filters: Record<string, NullableFilter>) {

      if (!this.filters[category]) {
        this.filters[category] = {
          ...this.filters.default
        }
      }

      for (const key of Object.keys(filters)) {
        if (filters[key] !== null) {
          this.filters[category] = {
            ...this.filters[category],
            [key]: filters[key]
          }
        } else {
          delete this.filters[category][key]
        }
      }
    },
    updateItem(id: number, update: Partial<FeedItem>) {
      this.items = this.items.map((item: FeedItem) => {
        if (item.id === id) {
          return {
            ...item,
            ...update
          }
        }

        return item
      })
    },
    appendItems(items: FeedItem[]) {
      this.items = this.items.concat(items)
    },
    async fetchByUrl(url: string, initial: boolean = true) {
      if (initial) {
        this.isLoading = true
        this.items = []
      }

      const response = await fetch(url)
        .then(response => response.json())

      if (initial) {
        this.items = response.results
      } else {
        this.items = this.items.concat(response.results)
      }

      if (initial) {
        this.isLoading = false
      }

      return response
    }
  }
})
