import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/axios';
import { Pedido } from '../types/pedido';

const API_URL = '/pedidos';

// Fetch all pedidos
const fetchPedidos = async (limit = 100, offset = 0): Promise<Pedido[]> => {
  const response = await apiClient.get<Pedido[]>(API_URL, {
    params: { limit, offset },
  });
  return response.data;
};

// Fetch single pedido
const fetchPedido = async (id: number): Promise<Pedido> => {
  const response = await apiClient.get<Pedido>(`${API_URL}/${id}`);
  return response.data;
};

// Create pedido
const createPedido = async (
  data: Omit<Pedido, 'id' | 'created_at' | 'updated_at' | 'deleted_at'>
): Promise<Pedido> => {
  const response = await apiClient.post<Pedido>(API_URL, data);
  return response.data;
};

// Update pedido
const updatePedido = async (
  id: number,
  data: Omit<Pedido, 'id' | 'created_at' | 'updated_at' | 'deleted_at'>
): Promise<Pedido> => {
  const response = await apiClient.put<Pedido>(`${API_URL}/${id}`, data);
  return response.data;
};

// Delete pedido
const deletePedido = async (id: number): Promise<void> => {
  await apiClient.delete(`${API_URL}/${id}`);
};

// Transition estado
const transitionEstado = async (
  pedido_id: number,
  accion: string
): Promise<Pedido> => {
  const response = await apiClient.post<Pedido>(
    `${API_URL}/${pedido_id}/transition-estado`,
    {},
    { params: { accion } }
  );
  return response.data;
};

// Hooks
export const usePedidos = (limit = 100, offset = 0) => {
  return useQuery({
    queryKey: ['pedidos', limit, offset],
    queryFn: () => fetchPedidos(limit, offset),
  });
};

export const usePedido = (id: number) => {
  return useQuery({
    queryKey: ['pedido', id],
    queryFn: () => fetchPedido(id),
    enabled: !!id,
  });
};

export const useCreatePedido = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: Omit<Pedido, 'id' | 'created_at' | 'updated_at' | 'deleted_at'>) =>
      createPedido(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pedidos'] });
    },
  });
};

export const useUpdatePedido = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: number;
      data: Omit<Pedido, 'id' | 'created_at' | 'updated_at' | 'deleted_at'>;
    }) => updatePedido(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pedidos'] });
    },
  });
};

export const useDeletePedido = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => deletePedido(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pedidos'] });
    },
  });
};

export const useTransitionEstado = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ pedido_id, accion }: { pedido_id: number; accion: string }) =>
      transitionEstado(pedido_id, accion),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pedidos'] });
    },
  });
};
