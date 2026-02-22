const API_BASE_URL = 'http://localhost:8000/api/v1';

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

function getAuthHeaders(): Record<string, string> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  if (!token) return {};
  return { Authorization: `Bearer ${token}` };
}

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${url}`, {
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
      ...options?.headers
    },
    ...options
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
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
