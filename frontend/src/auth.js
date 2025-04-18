import axiosClient from './axiosClient';

// Set up axios interceptor to add the token to every request
export function setupAuthInterceptor() {
  axiosClient.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
}

// Initialize auth
export function initAuth() {
  setupAuthInterceptor();
}