import { defineStore } from 'pinia'

export interface Subscription {
  id: number
  title: string
  url: string
  description: string
  icon: string
  slug: string
  collections: number[]
  is_subscribed: boolean;
}

export interface SubscriptionsState {
  list: Subscription[]
  isLoading: boolean
}

export const useSubscriptionsStore = defineStore('subscriptions', {
  state: () => ({ list: [], isLoading: false }) as SubscriptionsState,
  getters: {
    userFeed(state: SubscriptionsState) {
      return state.list.filter((item) => item.is_subscribed)
    },
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
    feedsWithoutCollection() {
      // @ts-ignore
      return this.userFeed.filter((feed) => feed.collections.length === 0)
    }
  },
  actions: {
    setSubscriptions(feeds: Subscription[]) {
      this.list = feeds
    },
    updateCollections(id: number, collections: number[]) {
      const index = this.list.findIndex((el) => el.id === id)
      if (index > -1) {
        this.list[index] = {
          ...this.list[index],
          collections: [...this.list[index].collections, ...(collections ?? [])]
        }
      }
    },
    unsubscribe(id: number) {
      const index = this.list.findIndex((el) => el.id === id)
      this.list[index].is_subscribed = false
    },
    subscribe(subscription: Subscription) {
      const index = this.list.findIndex((el) => el.id === subscription.id)
      if (index > -1) {
        this.list.splice(index, 1, subscription)
      } else {
        this.list.push(subscription)
        this.list.sort((a, b) => a.title.localeCompare(b.title))
      }
    }
  }
})
