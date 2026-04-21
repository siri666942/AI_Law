<template>
  <div class="app">
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <svg width="32" height="32" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10 80L50 20L90 80H10Z" fill="white"/>
            <circle cx="30" cy="50" r="8" fill="white"/>
            <circle cx="70" cy="50" r="8" fill="white"/>
            <path d="M10 20H90" stroke="white" stroke-width="10" stroke-linecap="round"/>
          </svg>
          <span>法途</span>
        </div>
        <nav class="nav">
          <router-link to="/" class="nav-link" active-class="active">
            首页
          </router-link>
          <router-link to="/knowledge" class="nav-link" active-class="active">
            法律知识库
          </router-link>
          <router-link to="/process" class="nav-link" active-class="active">
            法律流程
          </router-link>
          <router-link to="/ai" class="nav-link" active-class="active">
            AI助手
          </router-link>
          <router-link to="/diagnosis" class="nav-link" active-class="active">
            智能诊断
          </router-link>
          <router-link to="/projects" class="nav-link" active-class="active">
            项目空间
          </router-link>
          <div v-if="isAuthenticated" class="auth-links">
            <span class="user-info">{{ currentUser?.username }}</span>
            <a href="#" class="nav-link" @click.prevent="handleLogout">退出</a>
          </div>
          <router-link v-else to="/login" class="nav-link auth-btn" active-class="active">
            登录/注册
          </router-link>
        </nav>
      </div>
    </header>
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { authApi } from './services/api'

const router = useRouter()
const isAuthenticated = ref(false)
const currentUser = ref(authApi.getCurrentUser())

const syncAuthState = () => {
  isAuthenticated.value = authApi.isAuthenticated()
  currentUser.value = authApi.getCurrentUser()
}

const handleLogout = () => {
  authApi.logout()
  router.push('/login')
}

onMounted(() => {
  syncAuthState()
  window.addEventListener(authApi.eventName, syncAuthState)
  window.addEventListener('storage', syncAuthState)
})

onBeforeUnmount(() => {
  window.removeEventListener(authApi.eventName, syncAuthState)
  window.removeEventListener('storage', syncAuthState)
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: #f0f2f5;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 72px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
  font-size: 20px;
  font-weight: 700;
  white-space: nowrap;
}

.logo svg {
  width: 32px;
  height: 32px;
}

.logo span {
  color: #fff;
}

.nav {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.nav-link {
  padding: 8px 16px;
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  border-radius: 6px;
  transition: all 0.2s;
  white-space: nowrap;
}

.nav-link:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.15);
}

.nav-link.active {
  color: #667eea;
  background: #fff;
}

.auth-links {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
}

.user-info {
  color: rgba(255, 255, 255, 0.92);
  font-size: 14px;
  font-weight: 600;
}

.auth-btn {
  background: rgba(255, 255, 255, 0.16);
  border: 1px solid rgba(255, 255, 255, 0.18);
}

.auth-btn:hover {
  background: rgba(255, 255, 255, 0.24);
}

.main {
  flex: 1;
}
</style>
