import axios, { AxiosInstance, AxiosError } from 'axios';

export const TOKEN_KEY = 'refine-auth';
export const API_BASE_URL = 'https://staging-api.skai-tech.fr';

class ApiService {
  private instance: AxiosInstance;

  constructor() {
    this.instance = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor - add auth token
    this.instance.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem(TOKEN_KEY);
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - handle errors
    this.instance.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Handle auth errors - clear token and redirect
          localStorage.removeItem(TOKEN_KEY);
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth methods
  async login(credentials: { username?: string; email?: string; password: string }) {
    const response = await this.instance.post(
      '/auth/token',
      new URLSearchParams({
        grant_type: 'password',
        username: credentials.username || credentials.email || '',
        password: credentials.password,
        scope: '',
        client_id: 'string',
        client_secret: 'string',
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          accept: 'application/json',
        },
      }
    );
    return response.data;
  }

  async getUserIdentity() {
    const response = await this.instance.get('/auth/me');
    return response.data;
  }

  // Generic CRUD methods
  async get(url: string, params?: any) {
    const response = await this.instance.get(url, { params });
    return response.data;
  }

  async post(url: string, data?: any) {
    const response = await this.instance.post(url, data);
    return response.data;
  }

  async put(url: string, data?: any) {
    const response = await this.instance.put(url, data);
    return response.data;
  }

  async patch(url: string, data?: any) {
    const response = await this.instance.patch(url, data);
    return response.data;
  }

  async delete(url: string) {
    const response = await this.instance.delete(url);
    return response.data;
  }

  // Get the axios instance for custom requests
  getInstance() {
    return this.instance;
  }
}

// Export singleton instance
export const apiService = new ApiService();
export default apiService;
