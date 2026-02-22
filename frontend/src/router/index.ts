import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/cases',
    name: 'Cases',
    component: () => import('../views/CasesView.vue')
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('../views/ChatView.vue')
  },
  {
    path: '/knowledge',
    name: 'Knowledge',
    component: () => import('../views/KnowledgeView.vue')
  },
  {
    path: '/process',
    name: 'Process',
    component: () => import('../views/ProcessView.vue')
  },
  {
    path: '/ai',
    name: 'AI',
    component: () => import('../views/AIView.vue')
  },
  {
    path: '/diagnosis',
    name: 'Diagnosis',
    component: () => import('../views/DiagnosisView.vue')
  },
  {
    path: '/report',
    name: 'Report',
    component: () => import('../views/ReportView.vue')
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('../views/ProjectsView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
