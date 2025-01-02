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
import IconPlusCircle from '@/components/icons/IconPlusCircle.vue'
import IconFolderNew from '@/components/icons/IconFolderNew.vue'
import Dialog from '@/components/Dialog.vue'
import { useTemplateRef } from 'vue'

const subscriptionsStore = useSubscriptionsStore()
const collectionsStore = useCollectionsStore()

const subscriptionDialog = useTemplateRef('subscriptionDialog')
const collectionDialog = useTemplateRef('collectionDialog')

subscriptionsStore.isLoading = true
Promise.all([
  fetch('/api/v1/subscriptions/').then((res) => res.json()),
  fetch('/api/v1/collections/').then((res) => res.json())
]).then(([feeds, collections]) => {
  subscriptionsStore.setSubscriptions(feeds)
  collectionsStore.setCollections(collections)
  subscriptionsStore.isLoading = false
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
          <div class="sidebar-block-header-buttons">
            <Button @click="collectionDialog?.open()" size="sm" variant="text">
              <template v-slot:icon>
                <IconFolderNew />
              </template>
            </Button>
            <Button @click="subscriptionDialog?.open()" size="sm" variant="text">
              <template v-slot:icon>
                <IconPlusCircle />
              </template>
            </Button>
          </div>
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
              :key="feed?.slug"
              v-for="feed in collection.feeds"
              :to="`/${feed?.slug}`"
              v-slot="{ href, navigate }"
              custom
            >
              <Button :as="'a'" @click="navigate" :href="href" variant="ghost" size="sm">
                <img width="20" height="20" :alt="feed?.title" :src="feed?.icon" />
                {{ feed?.title }}
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
  <Dialog ref="subscriptionDialog">
    Subscription Dialog
  </Dialog>
  <Dialog ref="collectionDialog">
    Collection Dialog
  </Dialog>
</template>

<style>

</style>
