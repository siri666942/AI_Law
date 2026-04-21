<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <svg width="48" height="48" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10 80L50 20L90 80H10Z" fill="white" />
            <circle cx="30" cy="50" r="8" fill="white" />
            <circle cx="70" cy="50" r="8" fill="white" />
            <path d="M10 20H90" stroke="white" stroke-width="10" stroke-linecap="round" />
          </svg>
          <span>法途</span>
        </div>
        <h1 class="login-title">{{ isLogin ? '欢迎登录' : '创建账户' }}</h1>
        <p class="login-subtitle">{{ isLogin ? '进入法途继续处理案件与文档' : '选择身份并创建您的法途账户' }}</p>
      </div>

      <div v-if="!isLogin" class="role-selector">
        <button
          type="button"
          class="role-option"
          :class="{ active: formData.role === 'client' }"
          @click="formData.role = 'client'"
        >
          <div class="role-icon">👤</div>
          <div class="role-info">
            <div class="role-name">普通用户</div>
            <div class="role-desc">咨询法律问题，管理需求与材料</div>
          </div>
        </button>
        <button
          type="button"
          class="role-option"
          :class="{ active: formData.role === 'lawyer' }"
          @click="formData.role = 'lawyer'"
        >
          <div class="role-icon">⚖️</div>
          <div class="role-info">
            <div class="role-name">律师</div>
            <div class="role-desc">提供专业法律服务与项目支持</div>
          </div>
        </button>
      </div>

      <form class="login-form" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label class="form-label">用户名</label>
          <input
            v-model="formData.username"
            type="text"
            class="form-input"
            placeholder="请输入用户名"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label">密码</label>
          <input
            v-model="formData.password"
            type="password"
            class="form-input"
            placeholder="请输入密码"
            required
          />
        </div>

        <div v-if="!isLogin" class="form-group">
          <label class="form-label">邮箱</label>
          <input
            v-model="formData.email"
            type="email"
            class="form-input"
            placeholder="请输入邮箱（选填）"
          />
        </div>

        <div v-if="!isLogin" class="form-group">
          <label class="form-label">手机号</label>
          <input
            v-model="formData.phone"
            type="tel"
            class="form-input"
            placeholder="请输入手机号（选填）"
          />
        </div>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? '处理中...' : isLogin ? '登录' : '注册并进入' }}
        </button>
      </form>

      <div class="login-footer">
        <span>{{ isLogin ? '还没有账户？' : '已有账户？' }}</span>
        <a href="#" class="toggle-link" @click.prevent="toggleMode">
          {{ isLogin ? '立即注册' : '立即登录' }}
        </a>
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import { authApi } from '../services/api'
import type { LoginFormData, RegisterFormData, UserRole } from '../types/auth'

const router = useRouter()
const isLogin = ref(true)
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const formData = reactive({
  username: '',
  password: '',
  email: '',
  phone: '',
  role: 'client' as UserRole
})

const resetMessages = () => {
  errorMessage.value = ''
  successMessage.value = ''
}

const toggleMode = () => {
  isLogin.value = !isLogin.value
  resetMessages()
}

const redirectAfterAuth = () => {
  const role = authApi.getUserRole()
  router.push(role === 'lawyer' ? '/projects' : '/')
}

const handleSubmit = async () => {
  loading.value = true
  resetMessages()

  try {
    if (isLogin.value) {
      const loginData: LoginFormData = {
        username: formData.username,
        password: formData.password
      }
      const response = await authApi.login(loginData)
      authApi.setSession(response)
      successMessage.value = '登录成功，正在进入系统...'
      setTimeout(redirectAfterAuth, 500)
      return
    }

    const registerData: RegisterFormData = {
      username: formData.username,
      password: formData.password,
      email: formData.email || undefined,
      phone: formData.phone || undefined,
      role: formData.role
    }
    const response = await authApi.register(registerData)
    authApi.setSession(response)
    successMessage.value = '注册成功，正在进入系统...'
    setTimeout(redirectAfterAuth, 500)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '操作失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: calc(100vh - 72px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 24px;
  background:
    radial-gradient(circle at top left, rgba(118, 75, 162, 0.3), transparent 35%),
    linear-gradient(135deg, #5c6ac4 0%, #2c3e7a 100%);
}

.login-card {
  width: 100%;
  max-width: 520px;
  padding: 40px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 24px 80px rgba(25, 36, 77, 0.28);
}

.login-header {
  text-align: center;
  margin-bottom: 28px;
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.logo span {
  font-size: 30px;
  font-weight: 800;
  color: #5c6ac4;
}

.login-title {
  margin: 0 0 8px;
  font-size: 28px;
  color: #1f2a44;
}

.login-subtitle {
  margin: 0;
  color: #62708c;
  font-size: 14px;
}

.role-selector {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 24px;
}

.role-option {
  border: 1px solid #d7dcf2;
  border-radius: 16px;
  padding: 16px;
  background: #f7f9ff;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.2s ease;
}

.role-option.active {
  border-color: #5c6ac4;
  background: #eef1ff;
  box-shadow: 0 8px 20px rgba(92, 106, 196, 0.14);
}

.role-icon {
  font-size: 24px;
}

.role-name {
  font-weight: 700;
  color: #1f2a44;
}

.role-desc {
  margin-top: 4px;
  color: #6e7a95;
  font-size: 12px;
  line-height: 1.5;
}

.login-form {
  display: grid;
  gap: 16px;
}

.form-group {
  display: grid;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  font-weight: 600;
  color: #31415f;
}

.form-input {
  width: 100%;
  border: 1px solid #d5dbef;
  border-radius: 14px;
  padding: 14px 16px;
  font-size: 15px;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-input:focus {
  border-color: #5c6ac4;
  box-shadow: 0 0 0 4px rgba(92, 106, 196, 0.12);
}

.submit-btn {
  margin-top: 8px;
  border: none;
  border-radius: 14px;
  padding: 14px 18px;
  background: linear-gradient(135deg, #5c6ac4 0%, #764ba2 100%);
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-footer {
  margin-top: 20px;
  text-align: center;
  color: #5f6b85;
}

.toggle-link {
  margin-left: 8px;
  color: #5c6ac4;
  font-weight: 700;
  text-decoration: none;
}

.error-message,
.success-message {
  margin-top: 16px;
  border-radius: 14px;
  padding: 12px 14px;
  font-size: 14px;
}

.error-message {
  background: #fff1f2;
  color: #b42318;
}

.success-message {
  background: #ecfdf3;
  color: #027a48;
}

@media (max-width: 640px) {
  .login-card {
    padding: 28px 20px;
  }

  .role-selector {
    grid-template-columns: 1fr;
  }
}
</style>
