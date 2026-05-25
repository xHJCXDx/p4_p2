import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
<<<<<<< HEAD
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
=======
import { Categoria } from '../types/categoria';

const API_URL = 'http://localhost:8000/categorias';

// Fetch all categorias
const fetchCategorias = async (limit = 100, offset = 0): Promise<Categoria[]> => {
  const url = new URL(API_URL);
  url.searchParams.append('limit', limit.toString());
  url.searchParams.append('offset', offset.toString());

  const response = await fetch(url.toString());
  const result = await response.json();

  if (result.success && result.data) {
    const items = result.data.items || result.data;
    return Array.isArray(items) ? items : [];
  }
  return result;
>>>>>>> origin/main
};

// Fetch single categoria
const fetchCategoria = async (id: number): Promise<Categoria> => {
<<<<<<< HEAD
  const response = await apiClient.get<Categoria>(`${API_URL}/${id}`);
  return response.data;
=======
  const response = await fetch(`${API_URL}/${id}`);
  const result = await response.json();
  if (result.success && result.data) return result.data;
  return result;
>>>>>>> origin/main
};

// Create categoria
const createCategoria = async (
  data: Omit<Categoria, 'id' | 'created_at' | 'updated_at'>
): Promise<Categoria> => {
<<<<<<< HEAD
  const response = await apiClient.post<Categoria>(API_URL, data);
  return response.data;
=======
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) throw new Error('Error creating categoria');
  const result = await response.json();
  return result.data || result;
>>>>>>> origin/main
};

// Update categoria
const updateCategoria = async (
  id: number,
  data: Omit<Categoria, 'id' | 'created_at' | 'updated_at'>
): Promise<Categoria> => {
<<<<<<< HEAD
  const response = await apiClient.put<Categoria>(`${API_URL}/${id}`, data);
  return response.data;
=======
  const response = await fetch(`${API_URL}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) throw new Error('Error updating categoria');
  const result = await response.json();
  return result.data || result;
>>>>>>> origin/main
};

// Delete categoria
const deleteCategoria = async (id: number): Promise<void> => {
<<<<<<< HEAD
  await apiClient.delete(`${API_URL}/${id}`);
};

// Hooks
export const useCategorias = (limit = 100, offset = 0, parentId?: number) => {
  return useQuery({
    queryKey: ['categorias', limit, offset, parentId],
    queryFn: () => fetchCategorias(limit, offset, parentId),
=======
  const response = await fetch(`${API_URL}/${id}`, {
    method: 'DELETE',
  });

  if (!response.ok) throw new Error('Error deleting categoria');
};

// Hooks
export const useCategorias = (limit = 100, offset = 0) => {
  return useQuery({
    queryKey: ['categorias', limit, offset],
    queryFn: () => fetchCategorias(limit, offset),
>>>>>>> origin/main
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
