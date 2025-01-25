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
    getBySlug(state) {
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
          useSubscriptionsStore().userFeed.find((feed) => feed.id === id)
        ).filter(Boolean) as Subscription[]
        return {
          ...collection,
          feeds
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
    setList(collections: Collection[]) {
      this.list = collections
    },
    add(collection: Collection) {
      this.list.push(collection)
      const subscriptions = useSubscriptionsStore()
      for (const subId of collection.feeds) {
        subscriptions.updateCollections(subId, [collection.id])
      }
    },
    update(collection: Collection) {
      const idx = this.list.findIndex((el) => el.id === collection.id)
      if (idx >= 0) {
        this.list[idx] = {
          ...this.list[idx],
          ...collection
        }
      }
    }
  }
})
