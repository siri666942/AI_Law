import type { Project } from '../types/project'

export const mockProjects: Project[] = [
  {
    id: 'p1',
    name: '股权结构优化项目',
    type: '股权设计',
    description: '从诊断报告创建的股权结构优化项目',
    status: '进行中',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 3),
    members: [
      { id: 'm1', name: '王律师', role: '律师', avatar: '律' },
      { id: 'm2', name: '张三', role: '客户', avatar: '张' },
      { id: 'm3', name: '李助理', role: '助理', avatar: '李' }
    ],
    files: [
      { id: 'f1', name: '公司章程草案.docx', type: 'docx', size: '245KB', uploadedBy: '王律师', uploadedAt: new Date(Date.now() - 1000 * 60 * 60 * 2) },
      { id: 'f2', name: '股权架构设计方案.pdf', type: 'pdf', size: '1.2MB', uploadedBy: '王律师', uploadedAt: new Date(Date.now() - 1000 * 60 * 60 * 5) }
    ],
    tasks: [
      { id: 't1', title: '收集公司现有资料', status: '已完成', priority: '高', createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 2), assignee: '张三' },
      { id: 't2', title: '设计新的股权架构方案', status: '进行中', priority: '高', createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24), assignee: '王律师', dueDate: new Date(Date.now() + 1000 * 60 * 60 * 24 * 2) },
      { id: 't3', title: '准备股东会决议文件', status: '待处理', priority: '中', createdAt: new Date(Date.now() - 1000 * 60 * 60 * 12), assignee: '李助理' }
    ],
    messages: [
      { id: 'msg1', content: '大家好，这个项目是从诊断报告创建的，主要解决股权结构问题。', sender: '王律师', senderRole: '律师', timestamp: new Date(Date.now() - 1000 * 60 * 60 * 5), type: 'text' },
      { id: 'msg2', content: '好的，我已经上传了公司现有资料，请查看。', sender: '张三', senderRole: '客户', timestamp: new Date(Date.now() - 1000 * 60 * 60 * 4), type: 'text' },
      { id: 'msg3', content: '收到，我先看一下资料，然后准备方案。', sender: '王律师', senderRole: '律师', timestamp: new Date(Date.now() - 1000 * 60 * 60 * 3), type: 'text' }
    ]
  },
  {
    id: 'p2',
    name: '商标注册申请',
    type: '知识产权',
    description: '公司品牌商标注册申请',
    status: '进行中',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 7),
    members: [
      { id: 'm1', name: '王律师', role: '律师', avatar: '律' },
      { id: 'm2', name: '李四', role: '客户', avatar: '李' }
    ],
    files: [
      { id: 'f1', name: '商标查询报告.pdf', type: 'pdf', size: '890KB', uploadedBy: '王律师', uploadedAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 5) },
      { id: 'f2', name: '商标图样.jpg', type: 'jpg', size: '156KB', uploadedBy: '李四', uploadedAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 6) }
    ],
    tasks: [
      { id: 't1', title: '商标近似查询', status: '已完成', priority: '高', createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 6), assignee: '王律师' },
      { id: 't2', title: '准备商标注册申请材料', status: '进行中', priority: '高', createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 3), assignee: '王律师' },
      { id: 't3', title: '提交商标注册申请', status: '待处理', priority: '高', createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24), assignee: '王律师' }
    ],
    messages: [
      { id: 'msg1', content: '商标查询已完成，有一个近似商标但不影响注册。', sender: '王律师', senderRole: '律师', timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24 * 4), type: 'text' }
    ]
  }
]
