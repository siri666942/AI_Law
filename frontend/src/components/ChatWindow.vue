<template>
  <div class="chat-window">
    <div v-if="!currentSession" class="empty-state">
      <p>请选择一个会话开始聊天</p>
    </div>
    <div v-else class="chat-content">
      <div class="chat-window-header">
        <div class="header-left">
          <div class="header-avatar">{{ currentSession.avatar }}</div>
          <div class="header-info">
            <div class="header-name">{{ currentSession.clientName }}</div>
            <div class="header-status">在线</div>
          </div>
        </div>
      </div>
      <div class="messages-container" ref="messagesContainer">
        <div
          v-for="message in currentSession.messages"
          :key="message.id"
          class="message"
          :class="message.sender"
        >
          <div class="message-avatar" v-if="message.sender === 'client'">
            {{ currentSession.avatar }}
          </div>
          <div class="message-content-wrapper">
            <div class="message-bubble">
              {{ message.content }}
            </div>
            <div class="message-time">
              {{ formatMessageTime(message.timestamp) }}
            </div>
          </div>
          <div class="message-avatar lawyer" v-if="message.sender === 'lawyer'">
            律
          </div>
        </div>
      </div>
      <div class="input-area">
        <div class="input-wrapper">
          <textarea
            v-model="inputMessage"
            placeholder="输入消息..."
            @keydown.enter.prevent="sendMessage"
            rows="1"
            ref="textareaRef"
          ></textarea>
        </div>
        <button class="send-btn" @click="sendMessage" :disabled="!inputMessage.trim()">
          发送
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, onMounted } from 'vue'
import type { ChatSession, Message } from '../types/chat'

interface Props {
  currentSession: ChatSession | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'send', content: string): void
}>()

const inputMessage = ref('')
const messagesContainer = ref<HTMLElement>()
const textareaRef = ref<HTMLTextAreaElement>()

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

watch(() => props.currentSession?.messages, () => {
  scrollToBottom()
}, { deep: true })

onMounted(() => {
  scrollToBottom()
})

const sendMessage = () => {
  if (inputMessage.value.trim()) {
    emit('send', inputMessage.value)
    inputMessage.value = ''
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
    }
  }
}

const formatMessageTime = (date: Date) => {
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${hours}:${minutes}`
}
</script>

<style scoped>
.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
}

.empty-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 16px;
}

.chat-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-window-header {
  padding: 16px 24px;
  border-bottom: 1px solid #e8e8e8;
  background: #fafafa;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
}

.header-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.header-status {
  font-size: 12px;
  color: #52c41a;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: #f5f5f5;
}

.message {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.message.client {
  justify-content: flex-start;
}

.message.lawyer {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.message-avatar.lawyer {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.message-content-wrapper {
  max-width: 70%;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.message.client .message-content-wrapper {
  align-items: flex-start;
}

.message.lawyer .message-content-wrapper {
  align-items: flex-end;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  word-wrap: break-word;
}

.message.client .message-bubble {
  background: #fff;
  color: #333;
  border-bottom-left-radius: 4px;
}

.message.lawyer .message-bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-bottom-right-radius: 4px;
}

.message-time {
  font-size: 11px;
  color: #999;
  padding: 0 4px;
}

.input-area {
  padding: 16px 24px;
  border-top: 1px solid #e8e8e8;
  background: #fff;
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.input-wrapper {
  flex: 1;
}

.input-wrapper textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  resize: none;
  outline: none;
  transition: border-color 0.2s;
  max-height: 120px;
  min-height: 44px;
}

.input-wrapper textarea:focus {
  border-color: #667eea;
}

.send-btn {
  padding: 12px 28px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
