import { useMutation, useQuery } from '@tanstack/react-query';
import apiClient from '../api/axios';
import { useAuthStore, Usuario } from '../store/useAuthStore';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  nombre: string;
  email: string;
  password: string;
}

// Hook para login
export function useLogin() {
  const setUsuario = useAuthStore((state) => state.setUsuario);

  return useMutation({
    mutationFn: async (credentials: LoginCredentials) => {
      const response = await apiClient.post('/auth/login', credentials);
      const result = response.data;

      // El backend devuelve HTTP 200 incluso en errores, verificar success
      if (!result.success) {
        throw new Error(result.message || 'Credenciales inválidas');
      }

      return result.data || result;
    },
    onSuccess: () => {
      // Obtener datos del usuario después del login
      return apiClient.get('/auth/me').then((res) => {
        const userData = res.data.data || res.data;
        // Normalizar roles: backend envía [{codigo, descripcion}], frontend espera string[]
        if (userData.roles && userData.roles.length > 0 && typeof userData.roles[0] === 'object') {
          userData.roles = userData.roles.map((r: any) => r.codigo);
        }
        setUsuario(userData);
        return userData;
      });
    },
  });
}

// Hook para register
export function useRegister() {
  return useMutation({
    mutationFn: async (credentials: RegisterCredentials) => {
      const response = await apiClient.post('/auth/register', credentials);
      return response.data;
    },
  });
}

// Hook para logout
export function useLogout() {
  const logout = useAuthStore((state) => state.logout);

  return useMutation({
    mutationFn: async () => {
      await apiClient.post('/auth/logout');
    },
    onSuccess: () => {
      logout();
    },
  });
}

// Hook para obtener usuario actual (ejecuta al montar)
export function useCurrentUser() {
  const setUsuario = useAuthStore((state) => state.setUsuario);

  return useQuery({
    queryKey: ['auth', 'me'],
    queryFn: async () => {
      const response = await apiClient.get<Usuario>('/auth/me');
      setUsuario(response.data);
      return response.data;
    },
    retry: false, // No reintentar si falla (no autenticado)
    staleTime: 1000 * 60 * 5, // 5 minutos
  });
}
