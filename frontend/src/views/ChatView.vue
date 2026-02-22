<template>
  <div class="chat-view">
    <div class="chat-layout">
      <ChatList
        :chat-sessions="chatSessions"
        :selected-session-id="selectedSessionId"
        @select="handleSelectSession"
      />
      <ChatWindow
        :current-session="currentSession"
        @send="handleSendMessage"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import ChatList from '../components/ChatList.vue'
import ChatWindow from '../components/ChatWindow.vue'
import { mockChatSessions } from '../data/mockChats'
import type { ChatSession, Message } from '../types/chat'

const chatSessions = ref<ChatSession[]>(mockChatSessions)
const selectedSessionId = ref<string>(mockChatSessions[0].id)

const currentSession = computed(() => {
  return chatSessions.value.find(session => session.id === selectedSessionId.value) || null
})

const handleSelectSession = (sessionId: string) => {
  selectedSessionId.value = sessionId
  const session = chatSessions.value.find(s => s.id === sessionId)
  if (session) {
    session.unreadCount = 0
  }
}

const handleSendMessage = (content: string) => {
  const session = chatSessions.value.find(s => s.id === selectedSessionId.value)
  if (session) {
    const newMessage: Message = {
      id: `m${Date.now()}`,
      content,
      sender: 'lawyer',
      timestamp: new Date()
    }
    session.messages.push(newMessage)
    session.lastMessage = content
    session.lastMessageTime = new Date()

    setTimeout(() => {
      const replyMessage: Message = {
        id: `m${Date.now()}`,
        content: '收到您的消息，我会尽快回复您。',
        sender: 'client',
        timestamp: new Date()
      }
      session.messages.push(replyMessage)
      session.lastMessage = replyMessage.content
      session.lastMessageTime = new Date()
    }, 1500)
  }
}
</script>

<style scoped>
.chat-view {
  height: calc(100vh - 72px);
  background: #f5f5f5;
}

.chat-layout {
  display: flex;
  height: 100%;
  max-width: 1400px;
  margin: 0 auto;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
</style>
