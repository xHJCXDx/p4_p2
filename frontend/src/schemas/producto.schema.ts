import { z } from 'zod';

export const productoFormSchema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido').min(3, 'Mínimo 3 caracteres'),
  descripcion: z.string().min(1, 'La descripción es requerida'),
  precio_base: z.number().min(0.01, 'El precio debe ser mayor a 0'),
  imagen_url: z.string().optional().default(''),
  disponible: z.boolean().default(true),
  categoria_ids: z.array(z.number()).default([]),
});

export type ProductoFormType = z.infer<typeof productoFormSchema>;
