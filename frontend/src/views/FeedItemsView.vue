<script setup lang="ts">
import { defineProps, watch, ref } from 'vue'
import { onBeforeRouteLeave, useRoute } from 'vue-router'
import { useFeedStore } from '@/stores/feed.ts'
import FeedItem from '@/components/FeedItem.vue'
import { useSubscriptionsStore } from '@/stores/subscriptions.ts'
import { useCollectionsStore } from '@/stores/collections.ts'

const { feed_type } = defineProps({ feed_type: String })
const { getFeedBySlug } = useSubscriptionsStore()
const { getCollectionBySlug } = useCollectionsStore()
const feedStore = useFeedStore()
const route = useRoute()
const nextLink = ref(null)

function get_fetch_url_by_type() {
  switch (feed_type) {
    case 'feed':
      const feed = getFeedBySlug(route.params.slug)
      return `/api/v1/subscriptions/${feed?.id}/feed/`
    case 'collection':
      const collection = getCollectionBySlug(route.params.slug)
      return `/api/v1/collections/${collection?.id}/feed/`
    case 'favorites':
      return '/api/v1/favorites/'
    case 'podcasts':
      return '/api/v1/podcasts/'
    case 'videos':
      return '/api/v1/videos/'
    default:
      return '/api/v1/feed/'
  }
}

async function fetchFeed(url: string) {
  return fetch(url)
    .then((res) => res.json())
    .then((res) => {
      feedStore.appendItems(res.results)
      nextLink.value = res.next
    })
}

watch(get_fetch_url_by_type, (fetch_url) => {
  feedStore.$reset()
  fetchFeed(fetch_url)
})

function handleScroll(idx: number) {
  if (idx === feedStore.items.length - 1) {
    if (nextLink.value) {
      fetchFeed(nextLink.value)
    }
  }
}
</script>

<template>
  <ul class="feed-list-wrapper">
    <FeedItem
      v-for="(feedItem, idx) in feedStore.items"
      v-on:appear.once="handleScroll(idx)"
      :key="feedItem.id"
      :id="feedItem.id"
    />
  </ul>
</template>

<style scoped>
.feed-list-wrapper {
  display: flex;
  flex-direction: column;
  min-width: 0;
  padding: 0 0 calc(var(--grid-step) * 4);
  list-style: none;
}
</style>
