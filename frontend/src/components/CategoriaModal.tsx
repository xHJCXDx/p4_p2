import { useForm } from '@tanstack/react-form';
import { Categoria } from '../types/categoria';
import { categoriaFormSchema } from '../schemas/categoria.schema';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (categoria: Omit<Categoria, 'id'>) => void;
  categoriaInitial?: Categoria | null;
}

const CategoriaModal = ({ isOpen, onClose, onSubmit, categoriaInitial }: Props) => {
  const form = useForm({
    defaultValues: {
      nombre: categoriaInitial?.nombre || '',
      descripcion: categoriaInitial?.descripcion || '',
    },
    onSubmit: async ({ value }) => {
      const validated = categoriaFormSchema.parse(value);
      onSubmit(validated as Omit<Categoria, 'id'>);
      onClose();
    },
  });

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-md mx-4">
        <h2 className="text-2xl font-bold mb-6">
          {categoriaInitial ? 'Editar Categoría' : 'Nueva Categoría'}
        </h2>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            form.handleSubmit();
          }}
        >
          <form.Field
            name="nombre"
          >
            {(field) => (
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="nombre">
                  Nombre
                </label>
                <input
                  id="nombre"
                  type="text"
                  value={field.state.value}
                  onChange={(e) => field.handleChange(e.target.value)}
                  onBlur={field.handleBlur}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                />
                {field.state.meta.errors.map((error, idx) => (
                  <p key={idx} className="text-red-500 text-xs mt-1">
                    {error}
                  </p>
                ))}
              </div>
            )}
          </form.Field>

          <form.Field
            name="descripcion"
          >
            {(field) => (
              <div className="mb-6">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="descripcion">
                  Descripción
                </label>
                <textarea
                  id="descripcion"
                  rows={3}
                  value={field.state.value}
                  onChange={(e) => field.handleChange(e.target.value)}
                  onBlur={field.handleBlur}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                />
                {field.state.meta.errors.map((error, idx) => (
                  <p key={idx} className="text-red-500 text-xs mt-1">
                    {error}
                  </p>
                ))}
              </div>
            )}
          </form.Field>

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition-colors"
            >
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CategoriaModal;
