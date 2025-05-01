<script setup lang="ts">
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSubscriptionsStore } from '@/stores/subscriptions.ts'
import { useFeedStore } from '@/stores/feed.ts'
import { useCollectionsStore } from '@/stores/collections.ts'
import FeedList from '@/components/feed/List.vue'
import FeedFilters from '@/components/feed/Filters.vue'
import FeedSearch from '@/components/feed/Search.vue'
import FeedSubscription from '@/components/feed/Subscription.vue'
import FeedListLoader from '@/components/feed/Loader.vue'
import type { FeedType } from '@/utils/types.ts'
import { getFeedBaseUrl } from '@/utils/helpers.ts'

interface Props {
  feedType: FeedType
}

const route = useRoute()
const { feedType } = defineProps<Props>()
const subscriptions = useSubscriptionsStore()
const collections = useCollectionsStore()
const feedStore = useFeedStore()
const isLoading = computed(() => subscriptions.isLoading || collections.isLoading)

const currentSubscription = computed(() => {
  if (!route.params.slug) {
    return null
  }
  return subscriptions.getBySlug(route.params.slug as string)
})

const getEntityId = (feedType: FeedType): string | undefined => {
  if (feedType === 'subscription') {
    return subscriptions.getBySlug(route.params.slug as string)?.id?.toString()
  }

  if (feedType === 'collection') {
    return collections.getBySlug(route.params.slug as string)?.id?.toString()
  }

  return
}

const fetch_url = computed(() => {
  if (subscriptions.isLoading) {
    return null
  }

  switch(feedType) {
    case 'subscription':
      handleFiltersChange({ subscription_id: getEntityId(feedType) || null });
      break;
    case 'collection':
      handleFiltersChange({ collection_id: getEntityId(feedType) || null });
      break;
  }

  return getFeedBaseUrl(feedType, getEntityId(feedType))
})

function handleFiltersChange(filters: Record<string, string | null>) {
  const key = route.matched[0]?.name || route.name
  feedStore.setFilters(key as string, filters)
}

watch(() => route.matched[0]?.name || route.name, (_, prevName) => {
  feedStore.setFilters(prevName as string, { search: null, subscription_id: null, collection_id: null });
})
</script>

<template>
  <div class="section splitted">
    <section id="list" class="section list">
      <header class="feed-header">
        <FeedSearch :fetchUrl="fetch_url" @change="handleFiltersChange" />
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
      <FeedListLoader v-if="isLoading" />
      <FeedList v-else-if="fetch_url" :fetch-url="fetch_url" />
    </section>
    <section id="detail" class="section">
      <RouterView />
    </section>
  </div>
</template>

<style scoped></style>
