// Use the API base URL from environment variable
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '';

export interface ApiError {
  error?: string;
  detail?: string;
  message?: string;
}

// Get JWT token from localStorage
export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('token');
}

// Set JWT token in localStorage
export function setToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('token', token);
  }
}

// Remove JWT token from localStorage
export function removeToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token');
  }
}

// Handle 401 errors by redirecting to login
function handleUnauthorized(): void {
  removeToken();
  if (typeof window !== 'undefined') {
    window.location.href = '/login';
  }
}

// Base fetch function with auth headers
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers = new Headers({
    'Content-Type': 'application/json',
  });

  if (options.headers) {
    const extraHeaders = new Headers(options.headers as HeadersInit);
    extraHeaders.forEach((value, key) => {
      headers.set(key, value);
    });
  }

  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Unauthorized');
  }

  if (!response.ok) {
    const error: ApiError & { detail?: unknown } = await response.json().catch(() => ({}));

    let message: string | undefined;

    if (typeof error.error === 'string' && error.error) {
      message = error.error;
    } else if (typeof (error as any).detail === 'string') {
      message = (error as any).detail;
    } else if (Array.isArray((error as any).detail)) {
      const details = (error as any).detail as Array<{ msg?: string } & Record<string, unknown>>;
      const msgs = details
        .map((d) => d.msg)
        .filter((m): m is string => typeof m === 'string' && m.length > 0);
      if (msgs.length > 0) {
        message = msgs.join(', ');
      }
    }

    if (!message && typeof error.message === 'string' && error.message) {
      message = error.message;
    }

    throw new Error(message || 'Request failed');
  }

  return response.json();
}

// API functions

// Auth
export async function sendOTP(email: string): Promise<{ message: string }> {
  return apiRequest('/auth/send-otp', {
    method: 'POST',
    body: JSON.stringify({ email }),
  });
}

export async function verifyOTP(email: string, otp: string): Promise<{ token: string }> {
  return apiRequest('/auth/verify-otp', {
    method: 'POST',
    body: JSON.stringify({ email, otp }),
  });
}

// Projects
export interface Project {
  id: string;
  name: string;
  description: string | null;
  user_id: string;
  created_at: string;
}

export async function getProjects(): Promise<Project[]> {
  return apiRequest('/projects/');
}

export async function createProject(name: string, description: string): Promise<Project> {
  return apiRequest('/projects/', {
    method: 'POST',
    body: JSON.stringify({ name, description }),
  });
}

// Documents (File Upload)
export async function uploadDocument(projectId: string, file: File): Promise<{ status: string }> {
  const token = getToken();
  if (!token) {
    throw new Error('Not authenticated');
  }

  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/upload/${projectId}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
    body: formData,
  });

  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Unauthorized');
  }

  if (!response.ok) {
    const error: ApiError = await response.json().catch(() => ({}));
    throw new Error(error.error || error.detail || error.message || 'Upload failed');
  }

  return response.json();
}

// Agent
export interface AgentRunRequest {
  project_id: string;
  goal: string;
}

export interface AgentRunResponse {
  final_output: string | null;
  status: string;
}

export async function runAgent(projectId: string, goal: string): Promise<AgentRunResponse> {
  return apiRequest('/agent/run', {
    method: 'POST',
    body: JSON.stringify({ project_id: projectId, goal }),
  });
}

