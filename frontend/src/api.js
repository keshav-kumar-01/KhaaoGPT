import axios from 'axios';

const api = axios.create({
  // Use VITE_API_URL from environment or fallback to production URL
  baseURL: import.meta.env.VITE_API_URL || 'https://khaao-gpt-api.vercel.app',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor — attach JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('khao_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor — handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('khao_token');
      localStorage.removeItem('khao_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
