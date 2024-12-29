<script setup lang="ts">
import { computed, watch, defineProps } from 'vue'
import { useRoute } from 'vue-router'
import { useFeedsStore } from '@/stores/feeds.ts'

const route = useRoute()

const store = useFeedsStore()

const currentFeed = computed(() => store.getFeedBySlug(route.params.slug))
</script>

<template>
  <div class="section splitted">
    <section id="feed-list-section" class="section list">
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
      <RouterView />
    </section>
    <section class="detail-section"></section>
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
}
</style>
