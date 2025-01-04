<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Button from '@/components/Button.vue'
import IconHome from '@/components/icons/IconHome.vue'
import IconFavorite from '@/components/icons/IconFavorite.vue'
import IconArticle from '@/components/icons/IconArticle.vue'
import IconHeadphones from '@/components/icons/IconHeadphones.vue'
import IconMovie from '@/components/icons/IconMovie.vue'
import { useSubscriptionsStore } from '@/stores/subscriptions'
import { type Collection, useCollectionsStore } from '@/stores/collections.ts'
import Openable from '@/components/Openable.vue'
import IconFolder from '@/components/icons/IconFolder.vue'
import IconPlusCircle from '@/components/icons/IconPlusCircle.vue'
import IconFolderNew from '@/components/icons/IconFolderNew.vue'
import SubscriptionDialog from '@/components/dialogs/SubscriptionDialog.vue'
import { inject, useTemplateRef } from 'vue'
import CollectionDialog from '@/components/dialogs/CollectionDialog.vue'
import IconSettings from '@/components/icons/IconSettings.vue'
import { Injection } from '@/utils/constants.ts'

const subscriptionsStore = useSubscriptionsStore()
const collectionsStore = useCollectionsStore()
const collectionsDialogRef = useTemplateRef("collectionDialog")

const dialogsController = inject(Injection.DialogController)

subscriptionsStore.isLoading = true
Promise.all([
  fetch('/api/v1/subscriptions/').then((res) => res.json()),
  fetch('/api/v1/collections/').then((res) => res.json()),
]).then(([feeds, collections]) => {
  subscriptionsStore.setSubscriptions(feeds)
  collectionsStore.setCollections(collections)
  subscriptionsStore.isLoading = false
})

function openSubscriptionDialog() {
  dialogsController?.showDialog('subscription-dialog')
}

function showCollectionDialog(id?: number) {
  dialogsController?.showDialog('collection-dialog')
  if (id) {
    collectionsDialogRef.value?.setCollection(collectionsStore.getById(id) as Collection)
  }
}
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
            <Button @click="showCollectionDialog()" size="sm" variant="text">
              <template v-slot:icon>
                <IconFolderNew />
              </template>
            </Button>
            <Button @click="openSubscriptionDialog()" size="sm" variant="text">
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
            <template v-slot:right>
              <Button @click="showCollectionDialog(collection.id)" variant="text" size="sm" title="Edit collection">
                <template v-slot:icon>
                  <IconSettings class="openable-control__icon" />
                </template>
              </Button>
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
  <SubscriptionDialog />
  <CollectionDialog ref="collectionDialog" />
</template>

<style></style>
