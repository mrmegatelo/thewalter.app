<script setup lang="ts">
import { useFeedStore } from '@/stores/feed.ts'
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

const feedStore = useFeedStore()
const feedItem = computed(() => feedStore.getItemById(Number(route.params.id)))
</script>

<template>
  <div class="feed-detail-container">
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
</style>
