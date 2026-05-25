import { z } from 'zod';

export const ingredienteFormSchema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido').min(3, 'Mínimo 3 caracteres'),
  descripcion: z.string().default(''),
  es_alergeno: z.boolean().default(false),
});

export type IngredienteFormType = z.infer<typeof ingredienteFormSchema>;
