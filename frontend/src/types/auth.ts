export type UserRole = 'client' | 'lawyer'

export interface AuthUser {
  id: number
  username: string
  role?: UserRole | null
  email?: string | null
  phone?: string | null
  avatar?: string | null
}

export interface LoginFormData {
  username: string
  password: string
}

export interface RegisterFormData {
  username: string
  password: string
  email?: string
  phone?: string
  role: UserRole
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: AuthUser
}
