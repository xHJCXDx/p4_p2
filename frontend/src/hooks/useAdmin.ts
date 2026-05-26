import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/axios';

interface Usuario {
  id: number;
  nombre: string;
  email: string;
  roles: string[];
  created_at: string;
}

interface GetUsuariosParams {
  limit?: number;
  offset?: number;
  rol?: string;
}

const API_URL = '/admin/usuarios';

// Fetch all usuarios
const fetchUsuarios = async (params: GetUsuariosParams = {}): Promise<Usuario[]> => {
  const { limit = 100, offset = 0, ...filters } = params;
  const queryParams: Record<string, any> = { limit, offset, ...filters };

  const response = await apiClient.get<any>(API_URL, { params: queryParams });
  return response.data.data.items || [];
};

// Update usuario
const updateUsuario = async (
  id: number,
  data: Partial<Omit<Usuario, 'id' | 'created_at'>>
): Promise<Usuario> => {
  const response = await apiClient.put<any>(`${API_URL}/${id}`, data);
  return response.data.data || response.data;
};

// Delete usuario
const deleteUsuario = async (id: number): Promise<void> => {
  await apiClient.delete(`${API_URL}/${id}`);
};

// Assign roles
const assignRoles = async (id: number, roles: string[]): Promise<Usuario> => {
  const response = await apiClient.post<any>(`${API_URL}/${id}/roles`, { roles });
  return response.data.data || response.data;
};

// Hooks
export const useUsuarios = (params: GetUsuariosParams = {}) => {
  return useQuery({
    queryKey: ['usuarios', params],
    queryFn: () => fetchUsuarios(params),
  });
};

export const useUpdateUsuario = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: number;
      data: Partial<Omit<Usuario, 'id' | 'created_at'>>;
    }) => updateUsuario(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['usuarios'] });
    },
  });
};

export const useDeleteUsuario = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => deleteUsuario(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['usuarios'] });
    },
  });
};

export const useAssignRoles = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, roles }: { id: number; roles: string[] }) =>
      assignRoles(id, roles),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['usuarios'] });
    },
  });
};
