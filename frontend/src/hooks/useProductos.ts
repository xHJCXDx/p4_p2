import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
<<<<<<< HEAD
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
=======
import { Producto } from '../types/producto';

const API_URL = 'http://localhost:8000/productos';

// Fetch all productos
const fetchProductos = async (limit = 100, offset = 0): Promise<Producto[]> => {
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

// Fetch single producto
const fetchProducto = async (id: number): Promise<Producto> => {
<<<<<<< HEAD
  const response = await apiClient.get<Producto>(`${API_URL}/${id}`);
  return response.data;
=======
  const response = await fetch(`${API_URL}/${id}`);
  const result = await response.json();
  if (result.success && result.data) return result.data;
  return result;
>>>>>>> origin/main
};

// Create producto
const createProducto = async (
  data: Omit<Producto, 'id' | 'created_at' | 'updated_at'>
): Promise<Producto> => {
<<<<<<< HEAD
  const response = await apiClient.post<Producto>(API_URL, data);
  return response.data;
=======
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) throw new Error('Error creating producto');
  const result = await response.json();
  return result.data || result;
>>>>>>> origin/main
};

// Update producto
const updateProducto = async (
  id: number,
  data: Omit<Producto, 'id' | 'created_at' | 'updated_at'>
): Promise<Producto> => {
<<<<<<< HEAD
  const response = await apiClient.put<Producto>(`${API_URL}/${id}`, data);
  return response.data;
=======
  const response = await fetch(`${API_URL}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) throw new Error('Error updating producto');
  const result = await response.json();
  return result.data || result;
>>>>>>> origin/main
};

// Delete producto
const deleteProducto = async (id: number): Promise<void> => {
<<<<<<< HEAD
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
=======
  const response = await fetch(`${API_URL}/${id}`, {
    method: 'DELETE',
  });

  if (!response.ok) throw new Error('Error deleting producto');
};

// Hooks
export const useProductos = (limit = 100, offset = 0) => {
  return useQuery({
    queryKey: ['productos', limit, offset],
    queryFn: () => fetchProductos(limit, offset),
>>>>>>> origin/main
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
<<<<<<< HEAD

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
=======
>>>>>>> origin/main
