export interface LawCategory {
  id: string
  name: string
  description: string
  laws: Law[]
}

export interface Law {
  id: string
  number: number
  name: string
  fullName: string
  category: string
  publishDate?: string
  effectiveDate?: string
  content?: string
}
