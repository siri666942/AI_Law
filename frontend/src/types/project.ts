export interface Project {
  id: string
  name: string
  type: string
  description?: string
  status: '进行中' | '已完成' | '暂停'
  createdAt: Date
  members: ProjectMember[]
  files: ProjectFile[]
  tasks: ProjectTask[]
  messages: ProjectMessage[]
}

export interface ProjectMember {
  id: string
  name: string
  role: '律师' | '客户' | '助理'
  avatar: string
}

export interface ProjectFile {
  id: string
  name: string
  type: string
  size: string
  uploadedBy: string
  uploadedAt: Date
}

export interface ProjectTask {
  id: string
  title: string
  description?: string
  assignee?: string
  status: '待处理' | '进行中' | '已完成'
  priority: '高' | '中' | '低'
  dueDate?: Date
  createdAt: Date
}

export interface ProjectMessage {
  id: string
  content: string
  sender: string
  senderRole: string
  timestamp: Date
  type: 'text' | 'file' | 'image'
  file?: ProjectFile
}
