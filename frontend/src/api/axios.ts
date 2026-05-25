import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  withCredentials: true, // Envía cookies automáticamente (JWT httpOnly)
});

// Interceptor de response para manejar 401 (no autenticado)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o no válido - redirigir a login
      window.location.href = '/admin/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
