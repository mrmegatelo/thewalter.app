import { defineStore } from 'pinia'
import { useSubscriptionsStore } from '@/stores/subscriptions.ts'

interface Collection {
  id: string
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
        )
        return {
          ...collection,
          feeds,
        }
      })
    },
  },
  actions: {
    setCollections(collections: Collection[]) {
      this.list = collections
    },
  },
})
