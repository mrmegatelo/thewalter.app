import { createRouter, createWebHistory } from 'vue-router'
import FeedView from '@/views/FeedView.vue'
import FeedItemDetail from '@/views/FeedItemDetail.vue'

const router = createRouter({
  history: createWebHistory('feed'),
  routes: [
    {
      path: '/',
      name: 'feed',
      component: FeedView,
      props: { feedType: 'generic' },
      children: [
        {
          path: 'items/:id',
          name: 'feed_item_detail',
          component: FeedItemDetail,
        },
      ],
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: FeedView,
      props: { feedType: 'favorites' },
      children: [
        {
          path: 'items/:id',
          name: 'favorites_detail',
          component: FeedItemDetail,
        },
      ],
    },
    {
      path: '/articles',
      name: 'articles',
      component: FeedView,
      props: { feedType: 'articles' },
      children: [
        {
          path: 'items/:id',
          name: 'articles_detail',
          component: FeedItemDetail,
        },
      ],
    },
    {
      path: '/podcasts',
      name: 'podcasts',
      component: FeedView,
      props: { feedType: 'podcasts' },
      children: [
        {
          path: 'items/:id',
          name: 'podcasts_detail',
          component: FeedItemDetail,
        },
      ],
    },
    {
      path: '/videos',
      name: 'videos',
      component: FeedView,
      props: { feedType: 'videos' },
      children: [
        {
          path: 'items/:id',
          name: 'videos_detail',
          component: FeedItemDetail,
        },
      ],
    },
    {
      path: '/collection/:slug',
      name: 'collection_feed_list',
      component: FeedView,
      props: { feedType: 'collection' },
      children: [
        {
          path: 'items/:id',
          name: 'collection_feed_item_detail',
          component: FeedItemDetail,
        },
      ],
    },
    {
      path: '/:slug',
      name: 'feed_list',
      component: FeedView,
      props: { feedType: 'subscription' },
      children: [
        {
          path: 'items/:id',
          name: 'feed_list_item_detail',
          component: FeedItemDetail,
        },
      ],
    },
  ],
})

export default router
