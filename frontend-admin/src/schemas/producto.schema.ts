import { z } from 'zod';

export const productoFormSchema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido').min(3, 'Minimo 3 caracteres'),
  descripcion: z.string().min(1, 'La descripcion es requerida'),
  precio_base: z.number().min(0.01, 'El precio debe ser mayor a 0'),
  imagen_url: z.string().optional().default(''),
  stock_cantidad: z.number().int().min(0, 'El stock no puede ser negativo').default(0),
  disponible: z.boolean().default(true),
  categoria_ids: z.array(z.number()).default([]),
  ingrediente_ids: z.array(z.number()).default([]),
});

export type ProductoFormType = z.infer<typeof productoFormSchema>;
