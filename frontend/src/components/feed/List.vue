<script setup lang="ts">
import ListItem from '@/components//feed/ListItem.vue'
import { useFeedStore } from '@/stores/feed.ts'
import { computed, ref, watchEffect } from 'vue'
import { useRoute } from 'vue-router'
import IconInboxEmpty from '@/components/icons/IconInboxEmpty.vue'
import Loader from '@/components/feed/Loader.vue'
import { buildUrlWithParams } from '@/utils/helpers.ts'

const { fetchUrl } = defineProps({ fetchUrl: String })
const nextLink = ref(null)
const route = useRoute()
const feedStore = useFeedStore()

const requestUrl = computed(() => {
  if (!fetchUrl) {
    return
  }

  const filtersKey = route.matched[0]?.name || route.name
  return buildUrlWithParams(fetchUrl, feedStore.getFilters(filtersKey as string))
})

function handleScroll(idx: number) {
  if (idx === feedStore.items.length - 1) {
    if (nextLink.value) {
      feedStore.fetchByUrl(nextLink.value, false).then((response) => {
          nextLink.value = response.next
      })
    }
  }
}

watchEffect(async () => {
  if (!requestUrl.value) {
    return
  }
  const response = await feedStore.fetchByUrl(requestUrl.value)
  nextLink.value = response.next
})

</script>

<template>
  <Loader v-if="feedStore.isLoading" />
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
