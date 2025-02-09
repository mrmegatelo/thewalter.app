<script setup lang="ts">
import ListItem from '@/components//feed/ListItem.vue'
import { useFeedStore } from '@/stores/feed.ts'
import { computed, ref, watchEffect } from 'vue'
import { useRoute } from 'vue-router'
import IconInboxEmpty from '@/components/icons/IconInboxEmpty.vue'

const { fetchUrl } = defineProps({ fetchUrl: String })
const nextLink = ref(null)
const route = useRoute()
const feedStore = useFeedStore()

const requestUrl = computed(() => {
  if (!fetchUrl) {
    return
  }
  const url = new URL(fetchUrl, window.location.origin)
  const filtersKey = route.matched[0]?.name || route.name
  for (const [filter, values] of Object.entries(feedStore.getFilters(filtersKey as string))) {
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
  <div v-else-if="feedStore.isEmpty" class="feed-list-empty-container">
    <div class="feed-list-empty">
      <IconInboxEmpty class="feed-list-empty-icon" />
      <p>There is nothing new yet.</p>
    </div>
  </div>
  <ul v-else class="feed-list-wrapper">
    <ListItem
      v-for="(feedItem, idx) in feedStore.items"
      v-on:appear.once="handleScroll(idx)"
      :key="feedItem.id"
      :id="feedItem.id"
    />
  </ul>
</template>

<style scoped></style>
