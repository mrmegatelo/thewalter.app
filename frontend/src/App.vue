<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Button from '@/components/Button.vue'
import IconHome from '@/components/icons/IconHome.vue'
import IconFavorite from '@/components/icons/IconFavorite.vue'
import IconArticle from '@/components/icons/IconArticle.vue'
import IconHeadphones from '@/components/icons/IconHeadphones.vue'
import IconMovie from '@/components/icons/IconMovie.vue'
import { useSubscriptionsStore } from '@/stores/subscriptions'
import { useCollectionsStore } from '@/stores/collections.ts'
import Openable from '@/components/Openable.vue'
import IconFolder from '@/components/icons/IconFolder.vue'

const subscriptionsStore = useSubscriptionsStore()
const collectionsStore = useCollectionsStore()

subscriptionsStore.isLoading = true;
Promise.all([
  fetch('/api/v1/subscriptions/').then((res) => res.json()),
  fetch('/api/v1/collections/').then((res) => res.json()),
]).then(([feeds, collections]) => {
  subscriptionsStore.setSubscriptions(feeds);
  collectionsStore.setCollections(collections);
  subscriptionsStore.isLoading = false;
})
</script>

<template>
  <div class="root-container">
    <aside id="sidebar" class="section sidebar">
      <a class="sidebar-logo" href="#">
        <img alt="thewalter.app logo" class="logo" src="@/assets/logo.svg" />
      </a>
      <div class="sidebar-block sidebar-block-content">
        <RouterLink to="/" v-slot="{ href, navigate }" custom>
          <Button :as="'a'" @click="navigate" :href="href" variant="ghost" size="sm">
            <template v-slot:icon>
              <IconHome />
            </template>
            Home
          </Button>
        </RouterLink>
        <RouterLink to="/favorites" v-slot="{ href, navigate }" custom>
          <Button :as="'a'" @click="navigate" :href="href" variant="ghost" size="sm">
            <template v-slot:icon>
              <IconFavorite filled />
            </template>
            Favorites
          </Button>
        </RouterLink>
        <RouterLink to="/articles" v-slot="{ href, navigate }" custom>
          <Button :as="'a'" @click="navigate" :href="href" variant="ghost" size="sm">
            <template v-slot:icon>
              <IconArticle />
            </template>
            Articles
          </Button>
        </RouterLink>
        <RouterLink to="/podcasts" v-slot="{ href, navigate }" custom>
          <Button :as="'a'" @click="navigate" :href="href" variant="ghost" size="sm">
            <template v-slot:icon>
              <IconHeadphones />
            </template>
            Podcasts
          </Button>
        </RouterLink>
        <RouterLink to="/videos" v-slot="{ href, navigate }" custom>
          <Button :as="'a'" @click="navigate" :href="href" variant="ghost" size="sm">
            <template v-slot:icon>
              <IconMovie />
            </template>
            Videos
          </Button>
        </RouterLink>
      </div>
      <div class="sidebar-block">
        <div class="sidebar-block-header">
          <h4>Feeds:</h4>
        </div>
        <div class="sidebar-block-content">
          <Openable :key="collection.id" v-for="collection in collectionsStore.feedsByCollection">
            <template v-slot:trigger>
              <RouterLink class="openable__link" :to="`/collection/${collection.slug}`">
                {{ collection.title }}
              </RouterLink>
            </template>
            <template v-slot:icon>
              <IconFolder />
            </template>
            <RouterLink
              v-for="feed in collection.feeds"
              :to="`/${feed.slug}`"
              v-slot="{ href, navigate }"
              custom
            >
              <Button :as="'a'" @click="navigate" :href="href" variant="ghost" size="sm">
                <img width="20" height="20" :alt="feed.title" :src="feed.icon" />
                {{ feed.title }}
              </Button>
            </RouterLink>
          </Openable>
          <RouterLink
            :key="feed.id"
            v-for="feed in subscriptionsStore.feedsWithoutCollection"
            :to="`/${feed.slug}`"
            v-slot="{ href, navigate }"
            custom
          >
            <Button :as="'a'" @click="navigate" :href="href" variant="ghost" size="sm">
              <img width="20" height="20" :alt="feed.title" :src="feed.icon" />
              {{ feed.title }}
            </Button>
          </RouterLink>
        </div>
      </div>
    </aside>
    <main class="section main">
      <RouterView />
    </main>
  </div>
</template>

<style>
.root-container {
  display: grid;
  grid-template-columns: 300px 1fr;
  height: 100vh;
}

.section {
  --side-padding: calc(var(--grid-step) * 3);
  --vertical-padding: calc(var(--grid-step) * 4);
  max-height: 100vh;
  overflow: auto;
  padding: var(--vertical-padding) var(--side-padding);
  position: relative;
  height: 100%;

  & + & {
    border-left: 1px solid var(--color-grey-200);
  }
}

.main,
.list,
.splitted {
  --side-padding: 0;
  --vertical-padding: 0;
}

.splitted {
  display: grid;
  grid-template-columns: 500px minmax(500px, 1fr);
}

.sidebar {
  --sidebar-bg: var(--color-grey-50);
  --side-padding: 0;
  --vertical-padding: 0;
  background-color: var(--sidebar-bg);
  padding-bottom: calc(var(--grid-step) * 4);
  max-height: 100vh;
  overflow: auto;
  color: var(--color-grey-900);
  display: flex;
  flex-direction: column;

  & a {
    color: inherit;
  }
}

.sidebar-logo {
  display: block;
  padding: calc(var(--grid-step) * 4) calc(var(--grid-step) * 3) calc(var(--grid-step) * 2);
}

.sidebar-block {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: calc(var(--grid-step) * 1);
  padding: calc(var(--grid-step) * 1) calc(var(--grid-step) * 3);
  width: 100%;
}

.sidebar-block--bottom {
  margin-top: auto;
}

.sidebar-block-content {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: calc(var(--grid-step) * 0.25);
  width: 100%;
}
</style>
