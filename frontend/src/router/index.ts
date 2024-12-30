import { createRouter, createWebHistory } from 'vue-router'
import FeedView from '@/views/FeedView.vue'
import FeedItemDetail from '@/views/FeedItemDetail.vue'

const router = createRouter({
  history: createWebHistory('feed'),
  scrollBehavior(to) {
    const el = to.name?.toString().endsWith('_item_detail') ? '#detail' : '#list'
    // FIXME: this is a dirty hack for scroll because the default scroll behaviour does not work properly
    document.querySelector(el)?.scrollTo(0, 0)
    return false
  },
  routes: [
    {
      path: '/',
      name: 'feed',
      component: FeedView,
      props: { feed_type: 'default' },
      children: [
        {
          path: 'items/:id',
          name: 'feed_item_detail',
          component: FeedItemDetail
        }
      ]
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: FeedView,
      props: { feed_type: 'favorites' },
      children: [
        {
          path: 'items/:id',
          name: 'favorites_detail',
          component: FeedItemDetail
        }
      ]
    },
    {
      path: '/articles',
      name: 'articles',
      component: FeedView,
      props: { feed_type: 'articles' },
      children: [
        {
          path: 'items/:id',
          name: 'articles_detail',
          component: FeedItemDetail
        }
      ]
    },
    {
      path: '/podcasts',
      name: 'podcasts',
      component: FeedView,
      props: { feed_type: 'podcasts' },
      children: [
        {
          path: 'items/:id',
          name: 'podcasts_detail',
          component: FeedItemDetail
        }
      ]
    },
    {
      path: '/videos',
      name: 'videos',
      component: FeedView,
      props: { feed_type: 'videos' },
      children: [
        {
          path: 'items/:id',
          name: 'videos_detail',
          component: FeedItemDetail
        }
      ]
    },
    {
      path: '/collection/:slug',
      name: 'collection_feed_list',
      component: FeedView,
      props: { feed_type: 'collection' },
      children: [
        {
          path: 'items/:id',
          name: 'collection_feed_item_detail',
          component: FeedItemDetail
        }
      ]
    },
    {
      path: '/:slug',
      name: 'feed_list',
      component: FeedView,
      props: { feed_type: 'feed' },
      children: [
        {
          path: 'items/:id',
          name: 'feed_list_item_detail',
          component: FeedItemDetail
        }
      ]
    }
  ]
})

export default router
