import { defineStore } from 'pinia'

interface FeedItem {
  description: string
  has_paid_content: boolean
  link: string
  preview: string
  pub_date: string
  title: string
  feed: number
  id: number
}

interface FeedState {
  items: FeedItem[]
  total: number
  isLoading: boolean
}

export const useFeedStore = defineStore('feed', {
  state: () => ({ items: [], total: 0, isLoading: false }) as FeedState,
  getters: {
    getItemById: (state: FeedState) => (id: number) => state.items.find((item) => item.id === id),
  },
  actions: {
    setItems(items: FeedItem[]) {
      this.items = items
    },
    appendItems(items: FeedItem[]) {
      this.items = this.items.concat(items)
    },
  },
})
