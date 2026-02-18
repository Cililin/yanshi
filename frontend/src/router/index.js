import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/layout/index.vue'

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/articles',
    children: [
      {
        path: 'articles',
        name: 'Articles',
        component: () => import('@/views/Articles/index.vue'),
        meta: { title: '时政文章', icon: 'Document' }
      },
      {
        path: 'article/:id',
        name: 'ArticleDetail',
        component: () => import('@/views/Articles/detail.vue'),
        meta: { title: '文章详情', hidden: true }
      },
      {
        path: 'knowledge',
        name: 'Knowledge',
        component: () => import('@/views/Knowledge/index.vue'),
        meta: { title: '知识点', icon: 'Reading' }
      },
      {
        path: 'knowledge/graph',
        name: 'KnowledgeGraph',
        component: () => import('@/views/Knowledge/Graph.vue'),
        meta: { title: '知识图谱', hidden: true }
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: () => import('@/views/Statistics/index.vue'),
        meta: { title: '统计分析', icon: 'DataAnalysis' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - 研时` : '研时 - 考研时政智能分析系统'
  next()
})

export default router
