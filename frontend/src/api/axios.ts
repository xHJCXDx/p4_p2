import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  withCredentials: true, // Envía cookies automáticamente (JWT httpOnly)
});

// Interceptor de response para manejar 401 (no autenticado)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const url = error.config?.url || '';
    const isAuthRoute = url.includes('/auth/');
    const isOnLoginPage = window.location.pathname === '/admin/login';

    // No redirigir si estamos en login o si es una ruta de auth
    if (error.response?.status === 401 && !isAuthRoute && !isOnLoginPage) {
      window.location.href = '/admin/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
