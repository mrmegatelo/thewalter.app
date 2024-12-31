<script setup lang="ts">
import { computed, defineProps } from 'vue'
import { useRoute } from 'vue-router'
import { useSubscriptionsStore } from '@/stores/subscriptions.ts'
import { useFeedStore } from '@/stores/feed.ts'
import { useCollectionsStore } from '@/stores/collections.ts'
import FeedList from '@/components/FeedList.vue'
import FeedFilters from '@/components/FeedFilters.vue'

const route = useRoute()
const { feed_type } = defineProps({ feed_type: String })
const subscriptions = useSubscriptionsStore()
const { getFeedBySlug } = subscriptions
const { getCollectionBySlug } = useCollectionsStore()
const feedStore = useFeedStore()

const currentFeed = computed(() => {
  if (!route.params.slug) {
    return null
  }
  return subscriptions.getFeedBySlug(route.params.slug as string)
})

const fetch_url = computed(() => {
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
      return '/api/v1/feed/?type=favorite'
    case 'articles':
      return '/api/v1/feed/?type=article'
    case 'podcasts':
      return '/api/v1/feed/?type=podcast'
    case 'videos':
      return '/api/v1/feed/?type=video'
    default:
      return '/api/v1/feed/?'
  }
})

function handleFiltersChange(formData: FormData) {
  const filters: Record<string, unknown> = {}
  for (const key of formData.keys()) {
    filters[key] = formData.getAll(key)
  }

  feedStore.setFilters(filters)
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
        <FeedFilters @change="handleFiltersChange" />
      </header>
      <FeedList v-if="fetch_url" :fetch-url="fetch_url" />
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
</style>
