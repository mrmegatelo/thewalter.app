<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Button from '@/components/Button.vue'
import IconHome from '@/components/icons/IconHome.vue'
import IconFavorite from '@/components/icons/IconFavorite.vue'
import IconArticle from '@/components/icons/IconArticle.vue'
import IconHeadphones from '@/components/icons/IconHeadphones.vue'
import IconMovie from '@/components/icons/IconMovie.vue'
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
    </aside>
    <main class="section main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
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
