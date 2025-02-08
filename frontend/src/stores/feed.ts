import { defineStore } from 'pinia'

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
  isLoading: boolean
}

export const useFeedStore = defineStore('feed', {
  state: () =>
    ({
      items: [],
      total: 0,
      isLoading: false,
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
          ...this.filters.default,
          ...filters as FilterRecord,
        }
      } else {
        for (const key of Object.keys(filters)) {
          if (filters[key] !== null) {
            this.filters[category] = {
              ...this.filters[category],
              [key]: filters[key],
            }
          } else {
            delete this.filters[category][key]
          }
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
    }
  }
})
