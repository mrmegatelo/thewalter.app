<script setup lang="ts">
import FeedItem from '@/components/FeedItem.vue'
import { useFeedStore } from '@/stores/feed.ts'
import { ref, watchEffect } from 'vue'

const { fetchUrl } = defineProps({ fetchUrl: String })
const nextLink = ref(null)

const feedStore = useFeedStore()

function handleScroll(idx: number) {
  if (idx === feedStore.items.length - 1) {
    if (nextLink.value) {
      fetchFeed(nextLink.value)
    }
  }
}

async function fetchFeed(url: string) {
  feedStore.isLoading = true
  return fetch(url)
    .then((res) => res.json())
    .then((res) => {
      feedStore.appendItems(res.results)
      nextLink.value = res.next
      feedStore.isLoading = false
    })
}

watchEffect(async () => {
  feedStore.$reset()
  await fetchFeed(fetchUrl)
})
</script>

<template>
  <div class="feed-list-loader" v-if="feedStore.isLoading">Loading...</div>
  <ul v-else class="feed-list-wrapper">
    <FeedItem
      v-for="(feedItem, idx) in feedStore.items"
      v-on:appear.once="handleScroll(idx)"
      :key="feedItem.id"
      :id="feedItem.id"
    />
  </ul>
</template>

<style scoped>
.feed-list-loader {
    padding: calc(var(--grid-step) * 2) calc(var(--grid-step) * 3);
}
.feed-list-wrapper {
  display: flex;
  flex-direction: column;
  min-width: 0;
  padding: 0 0 calc(var(--grid-step) * 4);
  list-style: none;
}
</style>
