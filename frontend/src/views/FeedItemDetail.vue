<script setup lang="ts">
import { useFeedStore } from '@/stores/feed.ts'
import { useRoute } from 'vue-router'
import { computed, watch } from 'vue'
import IconThumbDown from '@/components/icons/IconThumbDown.vue'
import IconFavorite from '@/components/icons/IconFavorite.vue'

const route = useRoute()

const feedStore = useFeedStore()
const feedItem = computed(() => feedStore.getItemById(Number(route.params.id)))

function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts?.pop().split(';').shift()
}

function toggleAction(action: string) {
  const appliedActionsSet = new Set(feedItem?.value?.actions)
  const url = new URL('/api/v1/feed/' + route.params.id + '/actions/' + action + '/', window.location.origin)
  const request = new Request(url, {
    method: appliedActionsSet.has(action) ? 'DELETE' : 'POST'
  })


  request.headers.append('X-CSRFToken', getCookie('csrftoken'))

  if (appliedActionsSet.has(action)) {
    appliedActionsSet.delete(action)
  } else {
    appliedActionsSet.add(action)
  }

  fetch(request).then(res => res.json()).then((res) => {
    feedStore.updateItem(feedItem.value?.id, { actions: Array.from(appliedActionsSet) })
  })
}

watch(feedItem, (item, prevItem) => {
  if (!item || item?.actions?.includes('view')) {
    return
  }

  toggleAction('view')
}, { immediate: true })

</script>

<template>
  <div class="feed-detail-container">
    <div class="feed-links-list-item-controls">
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
    <section v-if="feedItem?.preview" class="feed-detail-section">
      <img class="feed-detail-preview" :src="feedItem.preview" :alt="feedItem.title" />
    </section>
    <section class="feed-detail-section">
      <h1>{{ feedItem?.title }}</h1>
    </section>
    <section
      class="feed-detail-section feed-detail-description"
      v-html="feedItem?.description"
    ></section>
  </div>
</template>

<style>
.feed-detail {
  min-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feed-detail-container {
  display: flex;
  flex-direction: column;
  gap: calc(var(--grid-step) * 4);
  max-width: 560px;
  margin: 0 auto 64px auto;
  align-items: flex-start;
  align-self: flex-start;
  justify-self: flex-end;
  min-width: 0;
}

.feed-detail-section {
  width: 100%;
}

.feed-detail-preview {
  max-width: 100%;
  max-height: 240px;
  margin: 0 auto;
  border-radius: calc(var(--grid-step) * 1.25);
}

.feed-detail-description {
  h1,
  .h1 {
    margin-top: 1.5rem;
    margin-bottom: 3rem;
  }

  h2,
  .h2 {
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
  }

  h3,
  .h3 {
    margin-top: 1.5rem;
    margin-bottom: 0rem;
  }

  h4,
  .h4 {
    margin-top: 1.5rem;
    margin-bottom: 0rem;
  }

  h5,
  .h5 {
    margin-top: 1.5rem;
    margin-bottom: 0rem;
  }

  p,
  ul,
  ol,
  pre,
  table,
  blockquote {
    margin-top: 0rem;
    margin-bottom: 1.5rem;
  }

  pre {
    background-color: var(--color-grey-50);
    padding: calc(var(--grid-step) * 2) calc(var(--grid-step) * 2.5);
    border-radius: calc(var(--grid-step) * 2);
    overflow-x: auto;
  }

  video,
  img {
    max-width: 100%;
    height: auto;
  }

  figcaption {
    font-style: italic;
    font-size: 0.833rem;
    line-height: 1rem;
  }

  hr,
  .hr {
    border: 1px solid;
    margin: 1rem 0;
  }

  a,
  b,
  i,
  strong,
  em,
  small,
  code {
    line-height: 0;
  }

  sub,
  sup {
    line-height: 0;
    position: relative;
    vertical-align: baseline;
  }

  sup {
    top: -0.5em;
  }

  sub {
    bottom: -0.25em;
  }

  code {
    background-color: var(--color-grey-50);
    color: var(--color-orange-500);
    line-height: 1;
    padding: calc(var(--grid-step) * 0.5) calc(var(--grid-step) * 0.5);
    border-radius: 10px;
  }
}

.feed-detail__logo {
  opacity: 0.05;
}


.feed-links-list-item-controls {
  display: flex;
  gap: calc(var(--grid-step) * 1.5);
  align-items: center;
}
</style>
