export interface Producto {
  id: number;
  nombre: string;
  descripcion: string;
  precio_base: number;
  imagen_url?: string;
  disponible: boolean;
  categoria_ids?: number[];
  created_at?: string;
  updated_at?: string;
}

export interface ProductoCreate {
  nombre: string;
  descripcion: string;
  precio_base: number;
  imagen_url?: string;
  disponible?: boolean;
  categoria_ids?: number[];
}
