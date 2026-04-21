<template>
  <div class="chat-list">
    <div class="chat-header">
      <h3>会话列表</h3>
    </div>
    <div class="chat-sessions">
      <div
        v-for="session in chatSessions"
        :key="session.id"
        class="chat-session"
        :class="{ active: selectedSessionId === session.id }"
        @click="selectSession(session.id)"
      >
        <div class="session-avatar">{{ session.avatar }}</div>
        <div class="session-info">
          <div class="session-top">
            <span class="session-name">{{ session.clientName }}</span>
            <span class="session-time">{{ formatTime(session.lastMessageTime) }}</span>
          </div>
          <div class="session-bottom">
            <span class="session-message">{{ session.lastMessage || '暂无消息' }}</span>
            <span v-if="session.unreadCount > 0" class="session-badge">{{ session.unreadCount }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { ChatSession } from '../types/chat'

interface Props {
  chatSessions: ChatSession[]
  selectedSessionId: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'select', sessionId: string): void
}>()

const selectSession = (sessionId: string) => {
  emit('select', sessionId)
}

const formatTime = (date?: Date) => {
  if (!date) return ''
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString()
}
</script>

<style scoped>
.chat-list {
  width: 320px;
  background: #fff;
  border-right: 1px solid #e8e8e8;
  display: flex;
  flex-direction: column;
}

.chat-header {
  padding: 20px;
  border-bottom: 1px solid #e8e8e8;
}

.chat-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.chat-sessions {
  flex: 1;
  overflow-y: auto;
}

.chat-session {
  display: flex;
  gap: 12px;
  padding: 16px;
  cursor: pointer;
  transition: background 0.2s;
  border-bottom: 1px solid #f0f0f0;
}

.chat-session:hover {
  background: #f5f5f5;
}

.chat-session.active {
  background: #e6f7ff;
}

.session-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  flex-shrink: 0;
}

.session-info {
  flex: 1;
  min-width: 0;
}

.session-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.session-name {
  font-size: 15px;
  font-weight: 600;
  color: #333;
}

.session-time {
  font-size: 12px;
  color: #999;
  flex-shrink: 0;
  margin-left: 8px;
}

.session-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.session-message {
  font-size: 13px;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.session-badge {
  background: #ff4d4f;
  color: #fff;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  min-width: 20px;
  text-align: center;
  flex-shrink: 0;
  margin-left: 8px;
}
</style>
