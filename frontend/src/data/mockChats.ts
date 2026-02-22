import type { ChatSession, Message } from '../types/chat'

export const mockChatSessions: ChatSession[] = [
  {
    id: '1',
    clientName: '张三',
    lawyerName: '王律师',
    avatar: '张',
    lastMessage: '好的，我明天会准备好相关材料',
    lastMessageTime: new Date(Date.now() - 1000 * 60 * 30),
    unreadCount: 2,
    messages: [
      {
        id: 'm1',
        content: '王律师，您好，我想咨询一下合同纠纷的问题',
        sender: 'client',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2)
      },
      {
        id: 'm2',
        content: '你好，张三，请详细描述一下你的情况',
        sender: 'lawyer',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 1.9)
      },
      {
        id: 'm3',
        content: '我和李四签了一份买卖合同，但是他没有按时交货',
        sender: 'client',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 1.8)
      },
      {
        id: 'm4',
        content: '好的，合同有约定交货时间和违约责任吗？',
        sender: 'lawyer',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 1.7)
      },
      {
        id: 'm5',
        content: '有的，合同约定2024年1月15日前交货，逾期支付违约金',
        sender: 'client',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 1.6)
      },
      {
        id: 'm6',
        content: '那你可以准备以下材料：1. 合同原件 2. 付款凭证 3. 沟通记录',
        sender: 'lawyer',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 1.5)
      },
      {
        id: 'm7',
        content: '好的，我明天会准备好相关材料',
        sender: 'client',
        timestamp: new Date(Date.now() - 1000 * 60 * 30)
      }
    ]
  },
  {
    id: '2',
    clientName: '李四',
    lawyerName: '王律师',
    avatar: '李',
    lastMessage: '谢谢律师的建议！',
    lastMessageTime: new Date(Date.now() - 1000 * 60 * 60 * 3),
    unreadCount: 0,
    messages: [
      {
        id: 'm1',
        content: '律师，我想咨询一下劳动争议的问题',
        sender: 'client',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 5)
      },
      {
        id: 'm2',
        content: '你好，请说一下具体情况',
        sender: 'lawyer',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 4.9)
      },
      {
        id: 'm3',
        content: '公司无故辞退我，而且不给赔偿金',
        sender: 'client',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 4.8)
      },
      {
        id: 'm4',
        content: '你工作多久了？有劳动合同吗？',
        sender: 'lawyer',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 4.7)
      },
      {
        id: 'm5',
        content: '工作了3年，有劳动合同',
        sender: 'client',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 4.6)
      },
      {
        id: 'm6',
        content: '那你可以申请劳动仲裁，要求支付违法解除劳动合同的赔偿金',
        sender: 'lawyer',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 4)
      },
      {
        id: 'm7',
        content: '谢谢律师的建议！',
        sender: 'client',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 3)
      }
    ]
  }
]
