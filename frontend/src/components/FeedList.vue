<script setup lang="ts">
import FeedItem from '@/components/FeedItem.vue'
import { useFeedStore } from '@/stores/feed.ts'
import { computed, ref, watchEffect } from 'vue'
import { useRoute } from 'vue-router'

const { fetchUrl } = defineProps({ fetchUrl: String })
const nextLink = ref(null)
const route = useRoute()
const feedStore = useFeedStore()

const requestUrl = computed(() => {
  if (!fetchUrl) {
    return
  }
  const url = new URL(fetchUrl, window.location.origin)
  for (const [filter, values] of Object.entries(feedStore.getFilters(route.name as string))) {
    if (Array.isArray(values)) {
      values.forEach((value) => {
        url.searchParams.append(filter, value)
      })
    } else {
      url.searchParams.append(filter, values)
    }
  }

  return url.href
})

function handleScroll(idx: number) {
  if (idx === feedStore.items.length - 1) {
    if (nextLink.value) {
      fetchFeed(nextLink.value)
    }
  }
}

async function fetchFeed(url: string | URL) {
  return fetch(url)
    .then((res) => res.json())
    .then((res) => {
      feedStore.appendItems(res.results)
      nextLink.value = res.next
      feedStore.isLoading = false
    })
}

watchEffect(async () => {
  if (!requestUrl.value) {
    return
  }

  feedStore.isLoading = true
  feedStore.setItems([]);
  await fetchFeed(requestUrl.value)
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

<style scoped></style>
