<script setup lang="ts">
import { computed, defineProps } from 'vue'
import { useRoute } from 'vue-router'
import { useSubscriptionsStore } from '@/stores/subscriptions.ts'
import { useFeedStore } from '@/stores/feed.ts'
import { useCollectionsStore } from '@/stores/collections.ts'
import FeedList from '@/components/FeedList.vue'
import FeedFilters from '@/components/FeedFilters.vue'
import FeedSearch from '@/components/FeedSearch.vue'
import FeedSubscription from '@/components/FeedSubscription.vue'

const route = useRoute()
const { feed_type } = defineProps({ feed_type: String })
const subscriptions = useSubscriptionsStore()
const { getFeedBySlug } = subscriptions
const { getCollectionBySlug } = useCollectionsStore()
const feedStore = useFeedStore()

const currentSubscription = computed(() => {
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

function handleFiltersChange(filters: Record<string, string>) {
  const key = route.matched[0]?.name || route.name
  feedStore.setFilters(key as string, filters)
}
</script>

<template>
  <div class="section splitted">
    <section id="list" class="section list">
      <header class="feed-header">
        <FeedSearch @change="handleFiltersChange" />
        <div v-if="currentSubscription?.description" class="feed-description">
          <h3 class="heading">{{ currentSubscription?.title }}</h3>
          <p
            v-if="currentSubscription?.description"
            class="paragraph feed-description__text"
            title="{{ currentSubscription.description }}"
          >
            {{ currentSubscription.description }}
          </p>
        </div>
        <div v-if="currentSubscription">
          <FeedSubscription :feedId="currentSubscription.id" />
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

<style scoped></style>
