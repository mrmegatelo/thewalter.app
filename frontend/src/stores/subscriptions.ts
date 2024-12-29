import { defineStore } from 'pinia'

interface Feed {
  id: number
  title: string
  url: string
  description: string
  icon: string
  slug: string
  collections: number[]
}

interface FeedsState {
  list: Feed[]
  isLoading: boolean
}

export const useSubscriptionsStore = defineStore('subscriptions', {
  state: () => ({ list: [], isLoading: false }) as FeedsState,
  getters: {
    getFeedBySlug(state) {
      return (slug: string) => {
        if (state.isLoading) {
          return null
        }

        return state.list.find((feed) => feed.slug === slug)
      }
    },
    getFeedById(state) {
      return (id: number) => {
        if (state.isLoading) {
          return null
        }

        return state.list.find((feed) => feed.id === id)
      }
    },
    feedsWithoutCollection(state) {
      return state.list.filter((feed) => feed.collections.length === 0)
    },
  },
  actions: {
    setSubscriptions(feeds: Feed[]) {
      this.list = feeds
    },
  },
})
