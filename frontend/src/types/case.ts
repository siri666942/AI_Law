export interface LegalCase {
  id: string
  title: string
  caseNumber: string
  court: string
  caseType: string
  procedure: string
  year: number
  result: string
  parties: {
    plaintiff: string
    defendant: string
  }
  summary: string
  tags: string[]
  date: string
}

export interface FilterOptions {
  caseTypes: string[]
  courts: string[]
  procedures: string[]
  years: number[]
  results: string[]
}
