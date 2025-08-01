import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: {
      title: '首页 - 迈克尔逊干涉实验 AI 分析'
    }
  },
  {
    path: '/analysis',
    name: 'Analysis', 
    component: () => import('@/views/Analysis.vue'),
    meta: {
      title: '分析结果 - 迈克尔逊干涉实验 AI 分析'
    }
  }
]

export default routes