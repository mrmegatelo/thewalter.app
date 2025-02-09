<script setup lang="ts">
import { useFeedStore } from '@/stores/feed.ts'
import { computed, inject, onMounted, useTemplateRef } from 'vue'
import { useSubscriptionsStore } from '@/stores/subscriptions.ts'
import { useRoute } from 'vue-router'
import IconPaid from '@/components/icons/IconPaid.vue'
import { Injection } from '@/utils/constants.ts'
import type { IntlService } from '@/services/intl.ts'

const emit = defineEmits(['appear'])
const intlService = inject(Injection.Intl) as IntlService

const route = useRoute()
const { id } = defineProps({ id: Number })
const subscriptions = useSubscriptionsStore()
const feedStore = useFeedStore()
const feedItem = computed(() => {
  if (!id) {
    return
  }

  return feedStore.getItemById(id)
})
const feed = computed(() => {
  if (!feedItem.value) {
    return;
  }

  return subscriptions.getById(feedItem.value.feed)
})
const feedItemRef = useTemplateRef('feed-item')

onMounted(() => {
  if (!feedItemRef.value) {
    return
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        emit('appear')
      }
    })
  })

  observer.observe(feedItemRef.value)
})

function getDetailLinkParams() {
  const parentOrCurrentRoute = route.matched[0]
  const detailRoute = parentOrCurrentRoute.children[0]

  return {
    name: detailRoute.name,
    params: {
      slug: route.params.slug,
      id: feedItem.value?.id
    }
  }
}

function getFeedLinkParams() {
  return {
    name: 'feed_list',
    params: {
      slug: feed.value?.slug
    }
  }
}

function stripTags(htmlString: string) {
  // Create a new DOMParser instance
  const parser = new DOMParser()
  // Parse the HTML string
  const doc = parser.parseFromString(htmlString, 'text/html')
  // Extract text content
  const textContent = doc.body.textContent || ''
  // Trim whitespace
  return textContent.trim()
}
</script>

<template>
  <li v-if="feedItem" ref="feed-item" class="feed-links-list-item" :key="feedItem.id">
    <div class="feed-links-list-item-bloginfo">
      <RouterLink
        v-if="feed"
        :to="getFeedLinkParams()"
        class="feed-links-list-item-bloginfo__link link paragraph"
      >
        <img :src="feed.icon" height="16" width="16" />
        <small>{{ feed.title }}</small>
      </RouterLink>
      <small class="paragraph">
        {{ intlService.formatDate(new Date(feedItem.pub_date)) }}
      </small>
    </div>
    <RouterLink :to="getDetailLinkParams()" class="feed-links-list-item-link">
      <h4 class="heading feed-links-list-item__title">
        {{ feedItem.title }}
        <span
          v-if="feedItem?.has_paid_content"
          class="feed-item-feature feed-item-feature--paid"
          title="There may be paid content"
        >
          <IconPaid />
        </span>
      </h4>
    </RouterLink>
    <div v-if="feedItem.description" class="feed-links-list-item-body">
      <RouterLink :to="getDetailLinkParams()" class="feed-links-list-item-text">
        <p class="feed-links-list-item__description">{{ stripTags(feedItem.description) }}</p>
      </RouterLink>
    </div>
    <RouterLink
      class="feed-links-list-item-bloginfo-cover"
      :to="getDetailLinkParams()"
      :title="feedItem.title"
    >
      <img
        width="452"
        height="226"
        v-if="feedItem.preview"
        class="feed-links-list-item-bloginfo-cover__image"
        :src="feedItem.preview"
        :alt="feedItem.title"
      />
    </RouterLink>
  </li>
</template>

<style scoped></style>
