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
  slug: string
  feeds: number[]
}

interface FeedItem {
  description: string
  has_paid_content: boolean
  link: string
  preview: string
  pub_date: string
  title: string
  id: number
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
    getFeedById(state) {
      return (id: number) => {
        if (state.isLoading) {
          return null
        }

        return state.feeds.find((feed) => feed.id === id)
      }
    },
    getCollectionBySlug(state) {
      return (slug: string) => {
        if (state.isLoading) {
          return null
        }

        return state.collections.find((collection) => collection.slug === slug)
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
