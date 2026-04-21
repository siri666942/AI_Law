export interface Message {
  id: string
  content: string
  sender: 'lawyer' | 'client'
  timestamp: Date
  read?: boolean
}

export interface ChatSession {
  id: string
  clientName: string
  lawyerName: string
  avatar: string
  lastMessage?: string
  lastMessageTime?: Date
  unreadCount: number
  messages: Message[]
}
