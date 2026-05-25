import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/axios';
import { Categoria } from '../types/categoria';

const API_URL = '/categorias';

// Fetch all categorias
const fetchCategorias = async (limit = 100, offset = 0, parentId?: number): Promise<Categoria[]> => {
  const params: Record<string, any> = { limit, offset };
  if (parentId !== undefined) {
    params.parent_id = parentId;
  }

  const response = await apiClient.get<Categoria[]>(API_URL, { params });
  return response.data;
};

// Fetch single categoria
const fetchCategoria = async (id: number): Promise<Categoria> => {
  const response = await apiClient.get<Categoria>(`${API_URL}/${id}`);
  return response.data;
};

// Create categoria
const createCategoria = async (
  data: Omit<Categoria, 'id' | 'created_at' | 'updated_at'>
): Promise<Categoria> => {
  const response = await apiClient.post<Categoria>(API_URL, data);
  return response.data;
};

// Update categoria
const updateCategoria = async (
  id: number,
  data: Omit<Categoria, 'id' | 'created_at' | 'updated_at'>
): Promise<Categoria> => {
  const response = await apiClient.put<Categoria>(`${API_URL}/${id}`, data);
  return response.data;
};

// Delete categoria
const deleteCategoria = async (id: number): Promise<void> => {
  await apiClient.delete(`${API_URL}/${id}`);
};

// Hooks
export const useCategorias = (limit = 100, offset = 0, parentId?: number) => {
  return useQuery({
    queryKey: ['categorias', limit, offset, parentId],
    queryFn: () => fetchCategorias(limit, offset, parentId),
  });
};

export const useCategoria = (id: number) => {
  return useQuery({
    queryKey: ['categoria', id],
    queryFn: () => fetchCategoria(id),
    enabled: !!id,
  });
};

export const useCreateCategoria = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: Omit<Categoria, 'id' | 'created_at' | 'updated_at'>) =>
      createCategoria(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categorias'] });
    },
  });
};

export const useUpdateCategoria = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: number;
      data: Omit<Categoria, 'id' | 'created_at' | 'updated_at'>;
    }) => updateCategoria(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categorias'] });
    },
  });
};

export const useDeleteCategoria = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => deleteCategoria(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categorias'] });
    },
  });
};
