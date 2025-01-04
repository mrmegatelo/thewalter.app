import { defineStore } from 'pinia'
import { type Subscription, useSubscriptionsStore } from '@/stores/subscriptions.ts'

export interface Collection {
  id: number
  title: string
  slug: string
  feeds: number[]
}

interface FeedsState {
  list: Collection[]
  isLoading: boolean
}

export const useCollectionsStore = defineStore('collections', {
  state: () => ({ list: [], isLoading: false }) as FeedsState,
  getters: {
    getCollectionBySlug(state) {
      return (slug: string) => {
        if (state.isLoading) {
          return null
        }

        return state.list.find((collection) => collection.slug === slug)
      }
    },
    feedsByCollection(state) {
      return state.list.map((collection) => {
        const feeds = collection.feeds.map((id) =>
          useSubscriptionsStore().list.find((feed) => feed.id === id),
        ) as Subscription[]
        return {
          ...collection,
          feeds,
        }
      })
    },
    getById(state) {
      return (id: number) => {
        return state.list.find((feed) => feed.id === id)
      }
    }
  },
  actions: {
    setCollections(collections: Collection[]) {
      this.list = collections
    },
    addCollection(collection: Collection) {
      this.list.push(collection)
      const subscriptions = useSubscriptionsStore()
      for (const subId of collection.feeds) {
        subscriptions.updateCollections(subId, [collection.id])
      }
    },
  },
})
