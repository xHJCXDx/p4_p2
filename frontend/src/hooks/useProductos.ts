import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/axios';
import { Producto } from '../types/producto';

const API_URL = '/productos';

interface FetchProductosParams {
  limit?: number;
  offset?: number;
  categoria_id?: number;
  disponible?: boolean;
  busqueda?: string;
}

// Fetch all productos
const fetchProductos = async (params: FetchProductosParams = {}): Promise<Producto[]> => {
  const { limit = 100, offset = 0, ...filters } = params;
  const queryParams: Record<string, any> = { limit, offset, ...filters };

  const response = await apiClient.get<Producto[]>(API_URL, { params: queryParams });
  return response.data;
};

// Fetch single producto
const fetchProducto = async (id: number): Promise<Producto> => {
  const response = await apiClient.get<Producto>(`${API_URL}/${id}`);
  return response.data;
};

// Create producto
const createProducto = async (
  data: Omit<Producto, 'id' | 'created_at' | 'updated_at'>
): Promise<Producto> => {
  const response = await apiClient.post<Producto>(API_URL, data);
  return response.data;
};

// Update producto
const updateProducto = async (
  id: number,
  data: Omit<Producto, 'id' | 'created_at' | 'updated_at'>
): Promise<Producto> => {
  const response = await apiClient.put<Producto>(`${API_URL}/${id}`, data);
  return response.data;
};

// Delete producto
const deleteProducto = async (id: number): Promise<void> => {
  await apiClient.delete(`${API_URL}/${id}`);
};

// Update disponibilidad
const updateDisponibilidad = async (id: number, disponible: boolean): Promise<Producto> => {
  const response = await apiClient.patch<Producto>(`${API_URL}/${id}/disponibilidad`, {
    disponible,
  });
  return response.data;
};

// Hooks
export const useProductos = (params: FetchProductosParams = {}) => {
  return useQuery({
    queryKey: ['productos', params],
    queryFn: () => fetchProductos(params),
  });
};

export const useProducto = (id: number) => {
  return useQuery({
    queryKey: ['producto', id],
    queryFn: () => fetchProducto(id),
    enabled: !!id,
  });
};

export const useCreateProducto = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: Omit<Producto, 'id' | 'created_at' | 'updated_at'>) =>
      createProducto(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['productos'] });
    },
  });
};

export const useUpdateProducto = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: number;
      data: Omit<Producto, 'id' | 'created_at' | 'updated_at'>;
    }) => updateProducto(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['productos'] });
    },
  });
};

export const useDeleteProducto = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => deleteProducto(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['productos'] });
    },
  });
};

export const useUpdateDisponibilidad = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, disponible }: { id: number; disponible: boolean }) =>
      updateDisponibilidad(id, disponible),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['productos'] });
    },
  });
};
