<template>
  <div class="app">
    <header class="header">
      <div class="header-content">
        <h1 class="logo">律界法宝</h1>
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
        </nav>
      </div>
    </header>
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
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
  color: #fff;
  font-size: 20px;
  font-weight: 700;
  white-space: nowrap;
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

.main {
  flex: 1;
}
</style>
