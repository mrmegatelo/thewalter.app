import { createRouter, createWebHistory } from 'vue-router'
import FeedView from '@/views/FeedView.vue'

const router = createRouter({
  history: createWebHistory('feed'),
  routes: [
    {
      path: '/',
      name: 'root',
      component: FeedView,
      children: [
        {
          path: '/favorites',
          name: 'favorites',
          component: FeedView,
        },
        {
          path: '/articles',
          name: 'articles',
          component: FeedView,
        },
        {
          path: '/podcasts',
          name: 'podcasts',
          component: FeedView,
        },
        {
          path: '/videos',
          name: 'videos',
          component: FeedView,
        },
      ],
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

export default router
