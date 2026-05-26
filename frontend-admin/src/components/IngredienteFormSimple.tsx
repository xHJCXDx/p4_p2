import { useForm } from '@tanstack/react-form';
import { Ingrediente } from '../types/ingrediente';
import { ingredienteFormSchema } from '../schemas/ingrediente.schema';

interface IngredienteFormSimpleProps {
  onSubmit: (data: Omit<Ingrediente, 'id' | 'created_at' | 'updated_at'>) => Promise<void>;
  onCancel: () => void;
  initialData?: Ingrediente;
  isLoading?: boolean;
}

export function IngredienteFormSimple({
  onSubmit,
  onCancel,
  initialData,
  isLoading = false,
}: IngredienteFormSimpleProps) {
  const form = useForm({
    defaultValues: {
      nombre: initialData?.nombre || '',
      descripcion: initialData?.descripcion || '',
      es_alergeno: initialData?.es_alergeno || false,
    },
    onSubmit: async ({ value }) => {
      const validated = ingredienteFormSchema.parse(value);
      await onSubmit(validated as Omit<Ingrediente, 'id' | 'created_at' | 'updated_at'>);
    },
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        form.handleSubmit();
      }}
      className="space-y-4"
    >
      {/* Nombre */}
      <form.Field
        name="nombre"
      >
        {(field) => (
          <div>
            <label className="block text-gray-700 font-bold mb-2">Nombre *</label>
            <input
              type="text"
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
              onBlur={field.handleBlur}
              placeholder="Ej: Pollo, Leche, Cacahuetes"
              className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 ${
                field.state.meta.errors.length > 0 ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'
              }`}
            />
            {field.state.meta.errors.map((error, idx) => (
              <p key={idx} className="text-red-600 text-sm mt-1">
                {error}
              </p>
            ))}
          </div>
        )}
      </form.Field>

      {/* Descripción */}
      <form.Field
        name="descripcion"
      >
        {(field) => (
          <div>
            <label className="block text-gray-700 font-bold mb-2">Descripción</label>
            <textarea
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
              onBlur={field.handleBlur}
              placeholder="Descripción del ingrediente"
              rows={3}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            {field.state.meta.errors.map((error, idx) => (
              <p key={idx} className="text-red-600 text-sm mt-1">
                {error}
              </p>
            ))}
          </div>
        )}
      </form.Field>

      {/* Es Alergeno */}
      <form.Field name="es_alergeno">
        {(field) => (
          <div className="flex items-center">
            <input
              type="checkbox"
              checked={field.state.value}
              onChange={(e) => field.handleChange(e.target.checked)}
              onBlur={field.handleBlur}
              className="rounded focus:ring-2 focus:ring-blue-500"
            />
            <label className="ml-2 text-gray-700 font-bold">Marcar como alergeno</label>
          </div>
        )}
      </form.Field>

      {/* Botones */}
      <div className="flex gap-2 pt-4">
        <button
          type="submit"
          disabled={isLoading}
          className={`flex-1 font-bold py-2 px-4 rounded-lg transition-colors ${
            isLoading ? 'bg-gray-400 text-gray-600 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 text-white'
          }`}
        >
          {isLoading ? 'Guardando...' : initialData ? 'Actualizar' : 'Crear'}
        </button>
        <button
          type="button"
          onClick={onCancel}
          disabled={isLoading}
          className="flex-1 bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-lg transition-colors disabled:opacity-50"
        >
          Cancelar
        </button>
      </div>
    </form>
  );
}
