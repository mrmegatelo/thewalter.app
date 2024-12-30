<script setup lang="ts">
import { useFeedStore } from '@/stores/feed.ts'
import { onMounted, useTemplateRef } from 'vue'
import { useSubscriptionsStore } from '@/stores/subscriptions.ts'
import { useRoute } from 'vue-router'
import IconPaid from '@/components/icons/IconPaid.vue'

const emit = defineEmits(['appear'])

const route = useRoute()
const { id } = defineProps({ id: Number })
const { getFeedById } = useSubscriptionsStore()
const feedStore = useFeedStore()
const feedItem = feedStore.getItemById(id)
const feed = getFeedById(feedItem.feed)
const feedItemRef = useTemplateRef('feed-item')

onMounted(() => {
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
      id: feedItem.id,
    },
  }
}

function getFeedLinkParams() {
  return {
    name: 'feed_list',
    params: {
      slug: feed?.slug,
    },
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
  <li ref="feed-item" class="feed-links-list-item" :key="feedItem.id">
    <div class="feed-links-list-item-bloginfo">
      <RouterLink
        :to="getFeedLinkParams()"
        class="feed-links-list-item-bloginfo__link link paragraph"
      >
        <img :src="feed.icon" height="16" width="16" />
        <small>{{ feed.title }}</small>
      </RouterLink>
      <small class="paragraph">
        {{ feedItem.pub_date }}
      </small>
    </div>
    <RouterLink :to="getDetailLinkParams()" class="feed-links-list-item-link">
      <h4 class="heading feed-links-list-item__title">
        {{ feedItem.title }}
        <span v-if="feedItem?.has_paid_content" class="feed-item-feature feed-item-feature--paid" title="There may be paid content">
          <IconPaid />
        </span>
      </h4>
    </RouterLink>
    <div class="feed-links-list-item-body">
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

<style scoped>
.feed-links-list-item {
  display: flex;
  gap: calc(var(--grid-step) * 0.5);
  align-items: flex-start;
  flex-direction: column;
  padding: calc(var(--grid-step) * 2) calc(var(--grid-step) * 3) calc(var(--grid-step) * 3);
  transition: background-color 0.3s;

  &:hover {
    background-color: var(--color-grey-50);
  }
}

.feed-links-list-item-body {
  display: flex;
  gap: calc(var(--grid-step) * 1);
  align-items: flex-start;
  flex: 1;
  min-width: 0;
  width: 100%;
}

.feed-links-list-item-bloginfo {
  display: flex;
  gap: calc(var(--grid-step) * 2);
  margin-bottom: calc(var(--grid-step) * 0.5);
  align-items: center;
  justify-content: space-between;
  white-space: nowrap;
  align-self: stretch;
  font-weight: 500;
}

.feed-links-list-item-bloginfo__link {
  overflow: hidden;
  text-overflow: ellipsis;
  display: flex;
  align-items: center;
  gap: calc(var(--grid-step) * 0.5);

  & > * {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    min-width: 0;
  }
}

.feed-links-list-item-text {
  flex: 1;
  min-width: 0;
  text-decoration: none;
}

.feed-links-list-item-bloginfo-cover {
  border-radius: calc(var(--grid-step) * 2);
  margin-top: calc(var(--grid-step) * 0.5);
  overflow: hidden;
  border: none;
  position: relative;
  padding: 0;
}

.feed-links-list-item-bloginfo-cover__image {
  border-radius: calc(var(--grid-step) * 1.25);
  transition: filter 0.3s;
  object-fit: cover;
}

.feed-links-list-item-bloginfo-cover__text {
  position: absolute;
  top: 50%;
  left: 50%;
  display: flex;
  gap: calc(var(--grid-step) * 0.5);
  transform: translate(-50%, -50%);
  color: #fff;
  font-weight: bold;
  z-index: 2;
}

.feed-links-list-item-footer {
  display: flex;
  justify-content: space-between;
}

.feed-links-list-item-link {
  color: var(--color-grey-1000);
  text-decoration: none;
  width: 100%;
}

.feed-links-list-item__title {
  overflow: hidden;
  text-overflow: ellipsis;
}

.feed-links-list-item__description {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  -webkit-line-clamp: 5;
  color: var(--color-grey-600);
  font-size: 0.833rem;
  line-height: 1.25rem;
}

.feed-links-list-item__attachment {
  width: 100%;

  &.embed {
    aspect-ratio: 1.8;
    border: none;
    background-color: black;
  }
}

.feed-links-list-item-controls {
  display: flex;
  gap: calc(var(--grid-step) * 1.5);
  align-items: center;
}

.feed-links-list-item-controls__button {
  border: 1px solid var(--color-grey-100);

  &:hover {
    & .feed-links-list-item-controls__icon {
      filter: grayscale(0);
    }
  }
}

.feed-links-list-item-controls__icon {
  font-size: 20px;
  transition: filter 0.15s;
  filter: grayscale(1) contrast(50%);

  &.active {
    filter: grayscale(0);
  }
}

.feed-links-list-item:hover {
  & .feed-links-list-item-controls {
    pointer-events: auto;
  }
}

.feed-item-feature {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: calc(var(--grid-step) * 0.25);
    color: var(--color-orange-800);
    background-color: var(--color-orange-100);
    border-radius: var(--grid-step);
    width: calc(var(--grid-step) * 2.5);
    height: calc(var(--grid-step) * 2.5);
}

.feed-item-feature--paid {
    background-color: var(--color-yellow-200);
    color: var(--color-yellow-800);
}

</style>
