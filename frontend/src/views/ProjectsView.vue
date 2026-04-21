<template>
  <div class="projects-view">
    <div class="projects-layout">
      <div v-if="!selectedProject" class="project-list-section">
        <div class="section-header">
          <h2>项目协同空间</h2>
          <button class="create-btn" @click="showCreateModal = true">
            <span class="plus">+</span>
            新建项目
          </button>
        </div>

        <div class="project-list">
          <div
            v-for="project in projects"
            :key="project.id"
            class="project-card"
            :class="{ active: selectedProject?.id === project.id }"
            @click="selectProject(project)"
          >
            <div class="project-icon">{{ getProjectIcon(project.type) }}</div>
            <div class="project-info">
              <div class="project-name">{{ project.name }}</div>
              <div class="project-meta">
                <span class="project-type">{{ project.type }}</span>
                <span class="project-status" :class="getStatusClass(project.status)">{{ project.status }}</span>
              </div>
              <div class="project-stats">
                <span>📁 {{ project.files.length }} 文件</span>
                <span>✅ {{ getCompletedTasks(project) }}/{{ project.tasks.length }} 任务</span>
                <span>💬 {{ project.messages.length }} 消息</span>
              </div>
            </div>
            <div class="project-date">{{ formatDate(project.createdAt) }}</div>
          </div>
        </div>

        <div v-if="projects.length === 0" class="empty-state">
          <div class="empty-icon">📂</div>
          <h3>暂无项目</h3>
          <p>从诊断报告创建或手动创建您的第一个项目</p>
          <button class="create-empty-btn" @click="showCreateModal = true">创建新项目</button>
        </div>
      </div>

      <div v-else class="project-detail-section">
        <div class="detail-header">
          <button class="back-btn" @click="selectedProject = null">← 返回列表</button>
          <div class="header-content">
            <h2 class="detail-title">{{ selectedProject.name }}</h2>
            <div class="detail-meta">
              <span class="detail-type">{{ selectedProject.type }}</span>
              <span class="detail-status" :class="getStatusClass(selectedProject.status)">{{ selectedProject.status }}</span>
            </div>
          </div>
          <div class="header-actions">
            <button class="action-btn">📊 进度</button>
            <button class="action-btn">⚙️ 设置</button>
          </div>
        </div>

        <div class="detail-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            class="tab-btn"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            {{ tab.icon }} {{ tab.name }}
          </button>
        </div>

        <div class="tab-content">
          <div v-if="activeTab === 'overview'" class="overview-tab">
            <div class="overview-grid">
              <div class="stat-card">
                <div class="stat-icon">📋</div>
                <div class="stat-value">{{ selectedProject.tasks.length }}</div>
                <div class="stat-label">总任务</div>
              </div>
              <div class="stat-card">
                <div class="stat-icon">✅</div>
                <div class="stat-value">{{ getCompletedTasks(selectedProject) }}</div>
                <div class="stat-label">已完成</div>
              </div>
              <div class="stat-card">
                <div class="stat-icon">📁</div>
                <div class="stat-value">{{ selectedProject.files.length }}</div>
                <div class="stat-label">文件数</div>
              </div>
              <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-value">{{ selectedProject.members.length }}</div>
                <div class="stat-label">成员</div>
              </div>
            </div>

            <div class="overview-section">
              <h3 class="section-title">项目成员</h3>
              <div class="members-list">
                <div v-for="member in selectedProject.members" :key="member.id" class="member-item">
                  <div class="member-avatar">{{ member.avatar }}</div>
                  <div class="member-info">
                    <div class="member-name">{{ member.name }}</div>
                    <div class="member-role">{{ member.role }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="overview-section">
              <h3 class="section-title">最近动态</h3>
              <div class="activity-list">
                <div v-for="msg in selectedProject.messages.slice(-5).reverse()" :key="msg.id" class="activity-item">
                  <div class="activity-time">{{ formatTime(msg.timestamp) }}</div>
                  <div class="activity-content">
                    <span class="activity-user">{{ msg.sender }}</span>
                    发送了一条消息
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'files'" class="files-tab">
            <div class="files-header">
              <h3 class="section-title">文件区</h3>
              <button class="upload-btn">📤 上传文件</button>
            </div>
            <div class="files-list">
              <div v-for="file in selectedProject.files" :key="file.id" class="file-item">
                <div class="file-icon">{{ getFileIcon(file.type) }}</div>
                <div class="file-info">
                  <div class="file-name">{{ file.name }}</div>
                  <div class="file-meta">{{ file.size }} · {{ file.uploadedBy }} · {{ formatDate(file.uploadedAt) }}</div>
                </div>
                <div class="file-actions">
                  <button class="file-btn">下载</button>
                  <button class="file-btn">预览</button>
                </div>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'tasks'" class="tasks-tab">
            <div class="tasks-header">
              <h3 class="section-title">任务看板</h3>
              <button class="add-task-btn">+ 添加任务</button>
            </div>
            <div class="tasks-board">
              <div class="task-column">
                <div class="column-header">
                  <span class="column-title">待处理</span>
                  <span class="column-count">{{ getTasksByStatus(selectedProject, '待处理').length }}</span>
                </div>
                <div class="task-cards">
                  <div v-for="task in getTasksByStatus(selectedProject, '待处理')" :key="task.id" class="task-card">
                    <div class="task-priority" :class="task.priority.toLowerCase()">{{ task.priority }}</div>
                    <div class="task-title">{{ task.title }}</div>
                    <div class="task-meta">
                      <span v-if="task.assignee">👤 {{ task.assignee }}</span>
                      <span v-if="task.dueDate">📅 {{ formatDate(task.dueDate) }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="task-column">
                <div class="column-header">
                  <span class="column-title">进行中</span>
                  <span class="column-count">{{ getTasksByStatus(selectedProject, '进行中').length }}</span>
                </div>
                <div class="task-cards">
                  <div v-for="task in getTasksByStatus(selectedProject, '进行中')" :key="task.id" class="task-card">
                    <div class="task-priority" :class="task.priority.toLowerCase()">{{ task.priority }}</div>
                    <div class="task-title">{{ task.title }}</div>
                    <div class="task-meta">
                      <span v-if="task.assignee">👤 {{ task.assignee }}</span>
                      <span v-if="task.dueDate">📅 {{ formatDate(task.dueDate) }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="task-column">
                <div class="column-header">
                  <span class="column-title">已完成</span>
                  <span class="column-count">{{ getTasksByStatus(selectedProject, '已完成').length }}</span>
                </div>
                <div class="task-cards">
                  <div v-for="task in getTasksByStatus(selectedProject, '已完成')" :key="task.id" class="task-card completed">
                    <div class="task-priority" :class="task.priority.toLowerCase()">{{ task.priority }}</div>
                    <div class="task-title">{{ task.title }}</div>
                    <div class="task-meta">
                      <span v-if="task.assignee">👤 {{ task.assignee }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'chat'" class="chat-tab">
            <div class="chat-container">
              <div class="chat-messages" ref="chatMessagesRef">
                <div
                  v-for="msg in selectedProject.messages"
                  :key="msg.id"
                  class="chat-message"
                >
                  <div class="msg-avatar">{{ msg.sender.charAt(0) }}</div>
                  <div class="msg-wrapper">
                    <div class="msg-header">
                      <span class="msg-sender">{{ msg.sender }}</span>
                      <span class="msg-role" :class="msg.senderRole.toLowerCase()">{{ msg.senderRole }}</span>
                      <span class="msg-time">{{ formatTime(msg.timestamp) }}</span>
                    </div>
                    <div class="msg-content">{{ msg.content }}</div>
                  </div>
                </div>
              </div>
              <div class="chat-input-area">
                <textarea
                  v-model="newMessage"
                  placeholder="输入消息..."
                  rows="1"
                  @keydown.enter.prevent="sendMessage"
                ></textarea>
                <button class="send-btn" @click="sendMessage" :disabled="!newMessage.trim()">发送</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>创建新项目</h3>
          <button class="close-btn" @click="showCreateModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>项目名称</label>
            <input v-model="newProjectName" type="text" placeholder="请输入项目名称" />
          </div>
          <div class="form-group">
            <label>项目类型</label>
            <select v-model="newProjectType">
              <option value="股权设计">股权设计</option>
              <option value="知识产权">知识产权</option>
              <option value="合同审查">合同审查</option>
              <option value="劳动用工">劳动用工</option>
              <option value="融资合规">融资合规</option>
              <option value="其他">其他</option>
            </select>
          </div>
          <div class="form-group">
            <label>项目描述</label>
            <textarea v-model="newProjectDesc" rows="3" placeholder="请输入项目描述（可选）"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-btn cancel" @click="showCreateModal = false">取消</button>
          <button class="modal-btn confirm" @click="createProject">创建</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { mockProjects } from '../data/mockProjects'
import type { Project, ProjectMessage } from '../types/project'

const projects = ref<Project[]>([...mockProjects])
const selectedProject = ref<Project | null>(null)
const activeTab = ref('overview')
const showCreateModal = ref(false)
const newProjectName = ref('')
const newProjectType = ref('股权设计')
const newProjectDesc = ref('')
const newMessage = ref('')
const chatMessagesRef = ref<HTMLElement>()

const tabs = [
  { id: 'overview', name: '概览', icon: '📊' },
  { id: 'files', name: '文件', icon: '📁' },
  { id: 'tasks', name: '任务', icon: '✅' },
  { id: 'chat', name: '沟通', icon: '💬' }
]

const getProjectIcon = (type: string) => {
  const icons: Record<string, string> = {
    '股权设计': '🏢',
    '知识产权': '💡',
    '合同审查': '📄',
    '劳动用工': '👥',
    '融资合规': '💰'
  }
  return icons[type] || '📋'
}

const getFileIcon = (type: string) => {
  const icons: Record<string, string> = {
    docx: '📄',
    pdf: '📑',
    jpg: '🖼️',
    png: '🖼️'
  }
  return icons[type] || '📄'
}

const getStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    '进行中': 'active',
    '已完成': 'completed',
    '暂停': 'paused'
  }
  return classes[status] || ''
}

const getCompletedTasks = (project: Project) => {
  return project.tasks.filter(t => t.status === '已完成').length
}

const getTasksByStatus = (project: Project, status: string) => {
  return project.tasks.filter(t => t.status === status)
}

const formatDate = (date: Date) => {
  const d = new Date(date)
  return `${d.getMonth() + 1}月${d.getDate()}日`
}

const formatTime = (date: Date) => {
  const d = new Date(date)
  const now = new Date()
  const diff = now.getTime() - d.getTime()

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return formatDate(d)
}

const selectProject = (project: Project) => {
  selectedProject.value = project
  activeTab.value = 'overview'
}

const createProject = () => {
  if (!newProjectName.value.trim()) return

  const project: Project = {
    id: `p${Date.now()}`,
    name: newProjectName.value,
    type: newProjectType.value,
    description: newProjectDesc.value,
    status: '进行中',
    createdAt: new Date(),
    members: [
      { id: 'm1', name: '王律师', role: '律师', avatar: '律' },
      { id: 'm2', name: '您', role: '客户', avatar: '您' }
    ],
    files: [],
    tasks: [],
    messages: [
      {
        id: `msg${Date.now()}`,
        content: '项目已创建成功！欢迎来到项目协同空间。',
        sender: '系统',
        senderRole: '系统',
        timestamp: new Date(),
        type: 'text'
      }
    ]
  }

  projects.value.unshift(project)
  selectedProject.value = project
  showCreateModal.value = false
  newProjectName.value = ''
  newProjectDesc.value = ''
}

const sendMessage = () => {
  if (!newMessage.value.trim() || !selectedProject.value) return

  const message: ProjectMessage = {
    id: `msg${Date.now()}`,
    content: newMessage.value,
    sender: '您',
    senderRole: '客户',
    timestamp: new Date(),
    type: 'text'
  }

  selectedProject.value.messages.push(message)
  newMessage.value = ''

  nextTick(() => {
    if (chatMessagesRef.value) {
      chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
    }
  })
}

onMounted(() => {
  const savedResult = localStorage.getItem('lastDiagnosisResult')
  if (savedResult) {
    const result = JSON.parse(savedResult)
    const hasDiagnosisProject = projects.value.some(p => p.description?.includes('诊断报告'))
    if (!hasDiagnosisProject && result.risks.length > 0) {
      const project: Project = {
        id: `p${Date.now()}`,
        name: `${result.companyName}法律风险优化`,
        type: '综合顾问',
        description: '从诊断报告创建的法律风险优化项目',
        status: '进行中',
        createdAt: new Date(),
        members: [
          { id: 'm1', name: '王律师', role: '律师', avatar: '律' },
          { id: 'm2', name: '您', role: '客户', avatar: '您' }
        ],
        files: [],
        tasks: result.risks.slice(0, 3).map((risk: any, index: number) => ({
          id: `t${index}`,
          title: `解决${risk.title}问题`,
          description: risk.description,
          status: '待处理' as const,
          priority: risk.level,
          createdAt: new Date()
        })),
        messages: [
          {
            id: `msg1`,
            content: `已从诊断报告创建项目，发现${result.risks.length}个风险点需要处理。`,
            sender: '系统',
            senderRole: '系统',
            timestamp: new Date(),
            type: 'text'
          }
        ]
      }
      projects.value.unshift(project)
    }
  }
})
</script>

<style scoped>
.projects-view {
  height: calc(100vh - 64px);
  overflow: hidden;
}

.projects-layout {
  display: flex;
  height: 100%;
}

.project-list-section {
  width: 100%;
  padding: 24px;
  overflow-y: auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: #333;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.plus {
  font-size: 18px;
  line-height: 1;
}

.project-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.project-card {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: all 0.2s;
  align-items: center;
}

.project-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.project-card.active {
  border: 2px solid #667eea;
}

.project-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
}

.project-info {
  flex: 1;
}

.project-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}

.project-meta {
  display: flex;
  gap: 10px;
  margin-bottom: 8px;
}

.project-type {
  font-size: 13px;
  color: #667eea;
  background: #f5f7ff;
  padding: 4px 10px;
  border-radius: 4px;
}

.project-status {
  font-size: 13px;
  padding: 4px 10px;
  border-radius: 4px;
}

.project-status.active {
  color: #52c41a;
  background: #f6ffed;
}

.project-status.completed {
  color: #8c8c8c;
  background: #f5f5f5;
}

.project-stats {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #888;
}

.project-date {
  font-size: 13px;
  color: #999;
  flex-shrink: 0;
}

.empty-state {
  text-align: center;
  padding: 80px 24px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.empty-state h3 {
  font-size: 22px;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
}

.empty-state p {
  font-size: 14px;
  color: #666;
  margin-bottom: 24px;
}

.create-empty-btn {
  padding: 12px 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.create-empty-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.project-detail-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
  overflow: hidden;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
  background: #fafafa;
}

.back-btn {
  padding: 8px 14px;
  background: #f0f0f0;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #e8e8e8;
}

.header-content {
  flex: 1;
}

.detail-title {
  font-size: 20px;
  font-weight: 700;
  color: #333;
  margin-bottom: 4px;
}

.detail-meta {
  display: flex;
  gap: 10px;
}

.detail-type {
  font-size: 13px;
  color: #667eea;
  background: #f5f7ff;
  padding: 4px 10px;
  border-radius: 4px;
}

.detail-status {
  font-size: 13px;
  padding: 4px 10px;
  border-radius: 4px;
}

.detail-status.active {
  color: #52c41a;
  background: #f6ffed;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 8px 16px;
  background: #f0f0f0;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #e8e8e8;
}

.detail-tabs {
  display: flex;
  gap: 4px;
  padding: 12px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.tab-btn {
  padding: 10px 20px;
  background: transparent;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  background: #f5f5f5;
}

.tab-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.tab-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  padding: 24px;
  background: linear-gradient(135deg, #f5f7ff 0%, #f0f5ff 100%);
  border-radius: 12px;
  text-align: center;
}

.stat-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  color: #888;
}

.overview-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #333;
  margin-bottom: 16px;
}

.members-list {
  display: flex;
  gap: 16px;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #fafafa;
  border-radius: 10px;
}

.member-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
}

.member-name {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 2px;
}

.member-role {
  font-size: 13px;
  color: #888;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  gap: 16px;
  padding: 12px 16px;
  background: #fafafa;
  border-radius: 8px;
}

.activity-time {
  font-size: 13px;
  color: #999;
  flex-shrink: 0;
}

.activity-content {
  font-size: 14px;
  color: #333;
}

.activity-user {
  font-weight: 600;
  color: #667eea;
}

.files-header,
.tasks-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.upload-btn,
.add-task-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.upload-btn:hover,
.add-task-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.files-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.file-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #fafafa;
  border-radius: 10px;
  align-items: center;
}

.file-icon {
  font-size: 32px;
  flex-shrink: 0;
}

.file-info {
  flex: 1;
}

.file-name {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.file-meta {
  font-size: 13px;
  color: #888;
}

.file-actions {
  display: flex;
  gap: 8px;
}

.file-btn {
  padding: 6px 14px;
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.file-btn:hover {
  background: #f5f5f5;
}

.tasks-board {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.task-column {
  background: #fafafa;
  border-radius: 12px;
  padding: 16px;
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.column-title {
  font-size: 15px;
  font-weight: 700;
  color: #333;
}

.column-count {
  padding: 4px 10px;
  background: #e8e8e8;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  color: #666;
}

.task-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-card {
  padding: 16px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.task-card.completed {
  opacity: 0.7;
}

.task-priority {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 10px;
}

.task-priority.高 {
  background: #fff1f0;
  color: #ff4d4f;
}

.task-priority.中 {
  background: #fff7e6;
  color: #fa8c16;
}

.task-priority.低 {
  background: #f6ffed;
  color: #52c41a;
}

.task-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.task-meta {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: #888;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 260px);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 20px;
}

.chat-message {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.msg-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  flex-shrink: 0;
}

.msg-wrapper {
  flex: 1;
}

.msg-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.msg-sender {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.msg-role {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}

.msg-role.律师 {
  background: #f5f7ff;
  color: #667eea;
}

.msg-role.客户 {
  background: #f6ffed;
  color: #52c41a;
}

.msg-role.系统 {
  background: #f5f5f5;
  color: #888;
}

.msg-time {
  font-size: 12px;
  color: #999;
}

.msg-content {
  padding: 12px 16px;
  background: #f5f5f5;
  border-radius: 10px;
  font-size: 14px;
  color: #333;
  line-height: 1.6;
}

.chat-input-area {
  display: flex;
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.chat-input-area textarea {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #f0f0f0;
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
  resize: none;
  outline: none;
  transition: all 0.2s;
  max-height: 120px;
}

.chat-input-area textarea:focus {
  border-color: #667eea;
}

.send-btn {
  padding: 12px 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  align-self: flex-end;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  width: 480px;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #333;
}

.close-btn {
  width: 32px;
  height: 32px;
  background: #f5f5f5;
  border: none;
  border-radius: 50%;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #e8e8e8;
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #f0f0f0;
  border-radius: 10px;
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #667eea;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
  background: #fafafa;
}

.modal-btn {
  padding: 10px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.modal-btn.cancel {
  background: #f0f0f0;
  border: none;
  color: #666;
}

.modal-btn.cancel:hover {
  background: #e8e8e8;
}

.modal-btn.confirm {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: #fff;
}

.modal-btn.confirm:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
</style>
