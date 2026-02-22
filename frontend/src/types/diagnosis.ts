export interface DiagnosisQuestion {
  id: string
  order: number
  question: string
  type: 'single' | 'text'
  options?: string[]
  hint?: string
  riskTrigger?: (answer: string) => boolean
}

export interface DiagnosisAnswer {
  questionId: string
  answer: string
}

export interface RiskItem {
  id: string
  title: string
  description: string
  level: '高' | '中' | '低'
  scoreImpact: number
}

export interface DiagnosisResult {
  score: number
  risks: RiskItem[]
  summary: string
  suggestions: string[]
  companyName?: string
}
