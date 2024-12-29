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

interface Collection {
  id: string
  title: string
  feeds: number[]
}

interface FeedsState {
  feeds: Feed[]
  collections: Collection[]
  isLoading: boolean
}

export const useFeedsStore = defineStore('feeds', {
  state: () => ({ feeds: [], collections: [], isLoading: false }) as FeedsState,
  getters: {
    getFeedBySlug(state) {
      return (slug: string) => {
        if (state.isLoading) {
          return null
        }

        return state.feeds.find((feed) => feed.slug === slug)
      }
    },
    feedsByCollection(state) {
      return state.collections.map((collection) => {
        const feeds = collection.feeds.map((id) => this.feeds.find((feed) => feed.id === id))
        return {
          ...collection,
          feeds,
        }
      })
    },
    feedsWithoutCollection(state) {
      return state.feeds.filter((feed) => feed.collections.length === 0)
    },
  },
  actions: {
    setFeeds(feeds: Feed[]) {
      this.feeds = feeds
    },
    setCollections(collections: Collection[]) {
      this.collections = collections
    },
  },
})
