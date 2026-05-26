import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/axios';
import { Ingrediente } from '../types/ingrediente';

const API_URL = '/ingredientes';

// Fetch all ingredientes
const fetchIngredientes = async (limit = 100, offset = 0): Promise<Ingrediente[]> => {
  const response = await apiClient.get<any>(API_URL, {
    params: { limit, offset },
  });
  return response.data.data.items || [];
};

// Fetch single ingrediente
const fetchIngrediente = async (id: number): Promise<Ingrediente> => {
  const response = await apiClient.get<any>(`${API_URL}/${id}`);
  return response.data.data || response.data;
};

// Create ingrediente
const createIngrediente = async (
  data: Omit<Ingrediente, 'id' | 'created_at' | 'updated_at'>
): Promise<Ingrediente> => {
  const response = await apiClient.post<any>(API_URL, data);
  return response.data.data || response.data;
};

// Update ingrediente
const updateIngrediente = async (
  id: number,
  data: Omit<Ingrediente, 'id' | 'created_at' | 'updated_at'>
): Promise<Ingrediente> => {
  const response = await apiClient.put<any>(`${API_URL}/${id}`, data);
  return response.data.data || response.data;
};

// Delete ingrediente
const deleteIngrediente = async (id: number): Promise<void> => {
  await apiClient.delete(`${API_URL}/${id}`);
};

// Hooks
export const useIngredientes = (limit = 100, offset = 0) => {
  return useQuery({
    queryKey: ['ingredientes', limit, offset],
    queryFn: () => fetchIngredientes(limit, offset),
  });
};

export const useIngrediente = (id: number) => {
  return useQuery({
    queryKey: ['ingrediente', id],
    queryFn: () => fetchIngrediente(id),
    enabled: !!id,
  });
};

export const useCreateIngrediente = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: Omit<Ingrediente, 'id' | 'created_at' | 'updated_at'>) =>
      createIngrediente(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ingredientes'] });
    },
  });
};

export const useUpdateIngrediente = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: number;
      data: Omit<Ingrediente, 'id' | 'created_at' | 'updated_at'>;
    }) => updateIngrediente(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ingredientes'] });
    },
  });
};

export const useDeleteIngrediente = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => deleteIngrediente(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ingredientes'] });
    },
  });
};
