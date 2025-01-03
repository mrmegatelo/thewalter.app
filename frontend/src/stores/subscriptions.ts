import { defineStore } from 'pinia'

export interface Subscription {
  id: number
  title: string
  url: string
  description: string
  icon: string
  slug: string
  collections: number[]
}

export interface SubscriptionsState {
  list: Subscription[]
  isLoading: boolean
}

export const useSubscriptionsStore = defineStore('subscriptions', {
  state: () => ({ list: [], isLoading: false }) as SubscriptionsState,
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
    setSubscriptions(feeds: Subscription[]) {
      this.list = feeds
    },
  },
})
