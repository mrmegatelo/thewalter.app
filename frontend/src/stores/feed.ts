import { defineStore } from 'pinia'

interface FeedItem {
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

interface FeedState {
  items: FeedItem[]
  total: number
  filters: Record<string, Filter>
  isLoading: boolean
}

export const useFeedStore = defineStore('feed', {
  state: () =>
    ({
      items: [],
      total: 0,
      isLoading: false,
      filters: { exclude: ['viewed', 'not_interesting'] }
    }) as FeedState,
  getters: {
    getItemById: (state: FeedState) => (id: number) => state.items.find((item) => item.id === id),
    filterEnabled: (state: FeedState) => (name: string) => state.filters[name]
  },
  actions: {
    setItems(items: FeedItem[]) {
      this.items = items
    },
    setFilters(filters: Record<string, Filter>) {
      this.filters = filters
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
