import type { AuthUser, LoginFormData, LoginResponse, RegisterFormData, UserRole } from '../types/auth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface FilterParams {
  caseType?: string;
  court?: string;
  procedure?: string;
  year?: string;
  result?: string;
  keyword?: string;
}

export interface FilterOptions {
  caseTypes: string[];
  courts: string[];
  procedures: string[];
  years: number[];
  results: string[];
}

export interface LegalCase {
  id: string;
  title: string;
  caseNumber: string;
  court: string;
  caseType: string;
  procedure: string;
  year: number;
  result: string;
  parties: {
    plaintiff: string;
    defendant: string;
  };
  summary: string;
  tags: string[];
  date: string;
}

export interface GeneratedDocument {
  title: string;
  content: string;
}

export interface ReviewRisk {
  level: '高' | '中' | '低';
  text: string;
}

export interface ReviewResult {
  summary: string;
  risks: ReviewRisk[];
  suggestions: string[];
}

interface StreamEvent {
  type: 'chunk' | 'done' | 'error';
  content?: string;
  message?: string;
}

function getAuthHeaders(): Record<string, string> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  if (!token) return {};
  return { Authorization: `Bearer ${token}` };
}

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const isFormData = options?.body instanceof FormData;
  const headers: HeadersInit = {
    ...getAuthHeaders(),
    ...options?.headers
  };

  if (!isFormData && !(headers instanceof Headers) && !('Content-Type' in headers)) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers
  });

  if (!response.ok) {
    let errorMessage = `HTTP error! status: ${response.status}`;
    try {
      const errorPayload = await response.json();
      if (typeof errorPayload?.detail === 'string') {
        errorMessage = errorPayload.detail;
      } else if (typeof errorPayload?.message === 'string') {
        errorMessage = errorPayload.message;
      }
    } catch {
      // Ignore JSON parsing errors and keep the fallback message.
    }
    throw new Error(errorMessage);
  }

  const result: ApiResponse<T> = await response.json();
  
  if (!result.success) {
    throw new Error(result.message || '请求失败');
  }

  return result.data;
}

export const aiApi = {
  async ask(question: string): Promise<string> {
    const data = await request<{ answer: string }>('/ai/ask', {
      method: 'POST',
      body: JSON.stringify({ question })
    });
    return data.answer;
  },

  async askStream(
    question: string,
    handlers: {
      onChunk: (chunk: string) => void;
      onDone?: () => void;
    }
  ): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/ai/ask/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
      body: JSON.stringify({ question })
    });

    if (!response.ok) {
      let errorMessage = `HTTP error! status: ${response.status}`;
      try {
        const errorPayload = await response.json();
        if (typeof errorPayload?.detail === 'string') {
          errorMessage = errorPayload.detail;
        } else if (typeof errorPayload?.message === 'string') {
          errorMessage = errorPayload.message;
        }
      } catch {
        // Ignore JSON parsing errors and keep the fallback message.
      }
      throw new Error(errorMessage);
    }

    if (!response.body) {
      throw new Error('当前浏览器环境不支持流式响应。');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    const processEvent = (rawEvent: string) => {
      const dataLines = rawEvent
        .split('\n')
        .filter((line) => line.startsWith('data:'))
        .map((line) => line.slice(5).trim())
        .filter(Boolean);

      if (!dataLines.length) {
        return;
      }

      const payload = dataLines.join('\n');
      const event = JSON.parse(payload) as StreamEvent;

      if (event.type === 'chunk' && typeof event.content === 'string') {
        handlers.onChunk(event.content);
        return;
      }

      if (event.type === 'error') {
        throw new Error(event.message || '流式回复失败，请稍后重试。');
      }

      if (event.type === 'done') {
        handlers.onDone?.();
      }
    };

    while (true) {
      const { value, done } = await reader.read();
      buffer += decoder.decode(value || new Uint8Array(), { stream: !done });

      let separatorIndex = buffer.indexOf('\n\n');
      while (separatorIndex !== -1) {
        const rawEvent = buffer.slice(0, separatorIndex).trim();
        buffer = buffer.slice(separatorIndex + 2);
        if (rawEvent) {
          processEvent(rawEvent);
        }
        separatorIndex = buffer.indexOf('\n\n');
      }

      if (done) {
        const finalEvent = buffer.trim();
        if (finalEvent) {
          processEvent(finalEvent);
        }
        break;
      }
    }
  },

  async generateDocument(templateId: string, templateName: string, userPrompt?: string): Promise<GeneratedDocument> {
    return request<GeneratedDocument>('/ai/generate-document', {
      method: 'POST',
      body: JSON.stringify({ templateId, templateName, userPrompt })
    });
  },

  async reviewDocument(file: File, reviewFocus?: string): Promise<ReviewResult> {
    const formData = new FormData();
    formData.append('file', file);
    if (reviewFocus?.trim()) {
      formData.append('reviewFocus', reviewFocus.trim());
    }

    return request<ReviewResult>('/ai/review-document', {
      method: 'POST',
      body: formData
    });
  }
};

export const caseApi = {
  async getCases(params?: FilterParams): Promise<LegalCase[]> {
    const queryString = params 
      ? '?' + new URLSearchParams(params as Record<string, string>).toString()
      : '';
    return request<LegalCase[]>(`/cases${queryString}`);
  },

  async getLegalCases(): Promise<LegalCase[]> {
    return request<LegalCase[]>('/cases/legal-cases');
  },

  async getCaseById(id: string): Promise<LegalCase> {
    return request<LegalCase>(`/cases/${id}`);
  },

  async getFilterOptions(): Promise<FilterOptions> {
    return request<FilterOptions>('/cases/filters');
  },

  async checkHealth(): Promise<{ message: string; timestamp: string }> {
    return request('/health');
  }
};

const AUTH_CHANGED_EVENT = 'auth-changed';

function emitAuthChanged(): void {
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new Event(AUTH_CHANGED_EVENT));
  }
}

export const authApi = {
  eventName: AUTH_CHANGED_EVENT,

  async login(data: LoginFormData): Promise<LoginResponse> {
    return request<LoginResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  },

  async register(data: RegisterFormData): Promise<LoginResponse> {
    return request<LoginResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  },

  setSession(response: LoginResponse): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem('access_token', response.access_token);
    localStorage.setItem('user_info', JSON.stringify(response.user));
    emitAuthChanged();
  },

  logout(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_info');
    emitAuthChanged();
  },

  getCurrentUser(): AuthUser | null {
    if (typeof window === 'undefined') return null;
    const userInfo = localStorage.getItem('user_info');
    return userInfo ? JSON.parse(userInfo) as AuthUser : null;
  },

  isAuthenticated(): boolean {
    if (typeof window === 'undefined') return false;
    return !!localStorage.getItem('access_token');
  },

  getUserRole(): UserRole | null {
    return this.getCurrentUser()?.role ?? null;
  }
};
