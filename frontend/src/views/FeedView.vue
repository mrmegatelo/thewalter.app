<script setup lang="ts">
import { computed, defineProps, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSubscriptionsStore } from '@/stores/subscriptions.ts'
import FeedItem from '@/components/FeedItem.vue'
import { useFeedStore } from '@/stores/feed.ts'
import { useCollectionsStore } from '@/stores/collections.ts'

const route = useRoute()
const { feed_type } = defineProps({ feed_type: String })
const feedStore = useFeedStore()
const subscriptions = useSubscriptionsStore()
const { getFeedBySlug } = subscriptions
const { getCollectionBySlug } = useCollectionsStore()

const nextLink = ref(null)

const currentFeed = computed(() => {
  if (!route.params.slug) {
    return null
  }
  return subscriptions.getFeedBySlug(route.params.slug as string)
})

function get_fetch_url_by_type() {
  if (subscriptions.isLoading) {
    return null
  }

  switch (feed_type) {
    case 'feed':
      const feed = getFeedBySlug(route.params.slug as string)
      return `/api/v1/subscriptions/${feed?.id}/feed/`
    case 'collection':
      const collection = getCollectionBySlug(route.params.slug as string)
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
  if (!fetch_url) {
    return
  }

  feedStore.$reset()
  fetchFeed(fetch_url)
}, { immediate: true })

function handleScroll(idx: number) {
  if (idx === feedStore.items.length - 1) {
    if (nextLink.value) {
      fetchFeed(nextLink.value)
    }
  }
}
</script>

<template>
  <div class="section splitted">
    <section id="list" class="section list">
      <header class="feed-header">
        <div class="feed-description">
          <h3 class="heading">{{ currentFeed?.title }}</h3>
          <p
            v-if="currentFeed?.description"
            class="paragraph feed-description__text"
            title="{{ currentFeed.description }}"
          >
            {{ currentFeed.description }}
          </p>
        </div>
      </header>
      <ul class="feed-list-wrapper">
        <FeedItem
          v-for="(feedItem, idx) in feedStore.items"
          v-on:appear.once="handleScroll(idx)"
          :key="feedItem.id"
          :id="feedItem.id"
        />
      </ul>
    </section>
    <section id="detail" class="section">
      <RouterView />
    </section>
  </div>
</template>

<style scoped>
.feed-header {
  position: sticky;
  top: 0;
  background-color: var(--color-white);
  z-index: 20;
  padding: calc(var(--grid-step) * 4) calc(var(--grid-step) * 3) calc(var(--grid-step) * 2);
  border-bottom: 1px solid var(--color-grey-200);
  display: flex;
  flex-direction: column;
  gap: calc(var(--grid-step) * 2);
}

.feed-description {
  display: flex;
  flex-direction: column;
  gap: calc(var(--grid-step) * 0.5);
}

.feed-description__text {
  font-size: 0.833rem;
  line-height: 1.25rem;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  -webkit-line-clamp: 5;
  line-clamp: 5;
}

.feed-list-wrapper {
  display: flex;
  flex-direction: column;
  min-width: 0;
  padding: 0 0 calc(var(--grid-step) * 4);
  list-style: none;
}
</style>
