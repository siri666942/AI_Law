export interface LegalProcess {
  id: string
  title: string
  description: string
  businessType: string
  entityType: string
  industry: string
  region: string
  scenario: string
  steps: ProcessStep[]
  materials: string[]
  estimatedTime: string
  difficulty: '简单' | '中等' | '复杂'
}

export interface ProcessStep {
  order: number
  title: string
  description: string
  duration?: string
  tips?: string
}

export interface ProcessFilters {
  businessType: string
  entityType: string
  industry: string
  region: string
  scenario: string
}
