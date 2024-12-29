import { createRouter, createWebHistory } from 'vue-router'
import FeedView from '@/views/FeedView.vue'
import FeedItemDetail from '@/views/FeedItemDetail.vue'

const router = createRouter({
  history: createWebHistory('feed'),
  scrollBehavior(to) {
    const el = to.name === 'feed_item_detail' ? '#detail' : '#list'
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
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: FeedView,
      props: { feed_type: 'favorites' },
    },
    {
      path: '/articles',
      name: 'articles',
      component: FeedView,
      props: { feed_type: 'articles' },
    },
    {
      path: '/podcasts',
      name: 'podcasts',
      component: FeedView,
      props: { feed_type: 'podcasts' },
    },
    {
      path: '/videos',
      name: 'videos',
      component: FeedView,
      props: { feed_type: 'videos' },
    },
    {
      path: '/collection/:slug',
      name: 'collection_feed_list',
      component: FeedView,
      props: { feed_type: 'collection' },
    },
    {
      path: '/:slug',
      name: 'feed_list',
      component: FeedView,
      props: { feed_type: 'feed' },
      children: [
        {
          path: 'items/:id',
          name: 'feed_item_detail',
          component: FeedItemDetail,
        },
      ],
    },
  ],
})

export default router
