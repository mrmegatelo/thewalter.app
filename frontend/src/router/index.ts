import { createRouter, createWebHistory } from 'vue-router'
import FeedView from '@/views/FeedView.vue'
import AboutView from '@/views/AboutView.vue'
import FeedItemsView from '@/views/FeedItemsView.vue'

const router = createRouter({
  history: createWebHistory('feed'),
  routes: [
    {
      path: '/',
      name: 'root',
      component: FeedView,
      children: [
        {
          path: '/',
          name: 'feed',
          component: FeedItemsView,
          props: { feed_type: 'default' },
        },
        {
          path: '/favorites',
          name: 'favorites',
          component: FeedItemsView,
          props: { feed_type: 'favorites' },
        },
        {
          path: '/articles',
          name: 'articles',
          component: FeedItemsView,
          props: { feed_type: 'articles' },
        },
        {
          path: '/podcasts',
          name: 'podcasts',
          component: FeedItemsView,
          props: { feed_type: 'podcasts' },
        },
        {
          path: '/videos',
          name: 'videos',
          component: FeedItemsView,
          props: { feed_type: 'videos' },
        },
        {
          path: 'collection/:slug',
          name: 'collection_feed_list',
          component: FeedItemsView,
          props: { feed_type: 'collection' },
        },
        {
          path: '/:slug',
          name: 'feed_list',
          component: FeedItemsView,
          props: { feed_type: 'feed' },
        },
      ],
    },
  ],
})

export default router
