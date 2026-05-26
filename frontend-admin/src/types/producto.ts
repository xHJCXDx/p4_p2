export interface CategoriaInProducto {
  id: number;
  nombre: string;
}

export interface IngredienteInProducto {
  id: number;
  nombre: string;
  es_alergeno: boolean;
}

export interface Producto {
  id: number;
  nombre: string;
  descripcion: string;
  precio_base: number;
  imagen_url?: string;
  stock_cantidad: number;
  disponible: boolean;
  categorias: CategoriaInProducto[];
  ingredientes: IngredienteInProducto[];
  created_at?: string;
  updated_at?: string;
}

export interface ProductoCreate {
  nombre: string;
  descripcion: string;
  precio_base: number;
  imagen_url?: string;
  stock_cantidad?: number;
  disponible?: boolean;
  categoria_ids?: number[];
  ingrediente_ids?: number[];
}
