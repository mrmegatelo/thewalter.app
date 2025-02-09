<script setup lang="ts">
import { useFeedStore } from '@/stores/feed.ts'
import { useRoute } from 'vue-router'
import { computed, watch } from 'vue'
import IconThumbDown from '@/components/icons/IconThumbDown.vue'
import IconFavorite from '@/components/icons/IconFavorite.vue'
import { useSubscriptionsStore } from '@/stores/subscriptions.ts'
import IconLink from '@/components/icons/IconLink.vue'
import { getCookie } from '@/utils/helpers.ts'

const route = useRoute()

const feedStore = useFeedStore()
const subscriptions = useSubscriptionsStore()
const feedItem = computed(() => feedStore.getItemById(Number(route.params.id)))
const subscriptionUrl = computed(() => {
  if (!feedItem.value) {
    return null
  }

  const subscription = subscriptions.getById(feedItem.value.feed)
  if (!subscription) {
    return null
  }

  return new URL(subscription.url).hostname
})

function toggleAction(action: string) {
  if (!feedItem.value) {
    return
  }

  const appliedActionsSet = new Set(feedItem?.value?.actions)
  const url = new URL(
    '/api/v1/feed/' + route.params.id + '/actions/' + action + '/',
    window.location.origin
  )
  const request = new Request(url, {
    method: appliedActionsSet.has(action) ? 'DELETE' : 'POST'
  })

  request.headers.append('X-CSRFToken', getCookie('csrftoken'))

  if (appliedActionsSet.has(action)) {
    appliedActionsSet.delete(action)
  } else {
    appliedActionsSet.add(action)
  }

  fetch(request)
    .then((res) => res.json())
    .then(() => {
      // @ts-ignore
      feedStore.updateItem(feedItem.value?.id, { actions: Array.from(appliedActionsSet) })
    })
}

watch(
  feedItem,
  (item, prevItem) => {
    if (!item || item?.actions?.includes('view')) {
      return
    }

    toggleAction('view')
  },
  { immediate: true }
)
</script>

<template>
  <div class="feed-detail-container">
    <div v-if="feedItem" class="feed-links-list-item-controls">
      <button
        class="button button--ghost button--sm feed-links-list-item-controls__button"
        title="Like"
        @click="toggleAction('like')"
      >
        <span class="button__icon">
          <IconFavorite :filled="feedItem?.actions.includes('like')" />
        </span>
      </button>
      <button
        class="button button--ghost button--sm feed-links-list-item-controls__button"
        title="Not interesting"
        type="submit"
        @click="toggleAction('dislike')"
      >
        <span class="button__icon">
          <IconThumbDown :filled="feedItem?.actions.includes('dislike')" />
        </span>
      </button>
    </div>
    <section v-if="feedItem?.preview && !feedItem.attachments.length" class="feed-detail-section">
      <img class="feed-detail-preview" :src="feedItem.preview" :alt="feedItem.title" />
    </section>
    <section v-else-if="feedItem?.attachments.length" class="feed-detail-section">
      <div class="feed-detail-preview" :key="file.url" v-for="file in feedItem.attachments">
        <iframe v-if="file.type === 'embed'" class="feed-links-list-item__attachment embed"
                height="240"
                type="text/html"
                loading="lazy"
                referrerpolicy="strict-origin-when-cross-origin"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowfullscreen
                :src="file.url"
        ></iframe>
        <audio v-else-if="file.type === 'audio'" :src="file.url" controls></audio>
      </div>
    </section>
    <section class="feed-detail-section">
      <h1>{{ feedItem?.title }}</h1>
    </section>
    <section
      class="feed-detail-section feed-detail-description"
      v-html="feedItem?.description"
    ></section>
    <div class="feed-detail-section">
      <a
        v-if="feedItem && subscriptionUrl"
        :href="feedItem.link"
        class="button button--ghost button--sm button--outline"
        target="_blank"
      >
        <IconLink class="button__icon" />
        Read on {{ subscriptionUrl }}</a
      >
    </div>
  </div>
</template>

<style></style>
