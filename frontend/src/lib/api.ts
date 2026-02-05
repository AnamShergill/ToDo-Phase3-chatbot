import axios from 'axios';

// Configure axios with base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to add token to headers
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, redirect to login
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// Task API functions
export const taskApi = {
  // Get all tasks for current user
  getTasks: async (userId: number, params?: {
    page?: number;
    limit?: number;
    status?: string;
    priority?: string;
    sort?: string
  }) => {
    const queryParams = new URLSearchParams();
    if (params?.page) queryParams.append('skip', String((params.page - 1) * (params.limit || 10)));
    if (params?.limit) queryParams.append('limit', String(params.limit));
    if (params?.status) queryParams.append('status', params.status);
    if (params?.priority) queryParams.append('priority', params.priority);
    if (params?.sort) queryParams.append('sort', params.sort);

    const queryString = queryParams.toString();
    const url = `/api/${userId}/tasks${queryString ? `?${queryString}` : ''}`;

    const response = await api.get(url);
    return response.data;
  },

  // Create a new task
  createTask: async (userId: number, taskData: any) => {
    const response = await api.post(`/api/${userId}/tasks`, taskData);
    return response.data;
  },

  // Get a specific task
  getTask: async (userId: number, taskId: number) => {
    const response = await api.get(`/api/${userId}/tasks/${taskId}`);
    return response.data;
  },

  // Update a task
  updateTask: async (userId: number, taskId: number, taskData: any) => {
    const response = await api.put(`/api/${userId}/tasks/${taskId}`, taskData);
    return response.data;
  },

  // Update task completion status
  updateTaskCompletion: async (userId: number, taskId: number, completed: boolean) => {
    const response = await api.patch(`/api/${userId}/tasks/${taskId}/complete`, { completed });
    return response.data;
  },

  // Delete a task
  deleteTask: async (userId: number, taskId: number) => {
    const response = await api.delete(`/api/${userId}/tasks/${taskId}`);
    return response.data;
  },
};

// Auth API functions
export const authApi = {
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },

  register: async (email: string, password: string, name: string) => {
    const response = await api.post('/auth/register', { email, password, name });
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/auth/logout');
    return response.data;
  },
};