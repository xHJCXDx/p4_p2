import { useForm } from '@tanstack/react-form';
import { Producto } from '../types/producto';
import { productoFormSchema } from '../schemas/producto.schema';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (producto: Omit<Producto, 'id'>) => void;
  productoInitial?: Producto | null;
}

const ProductoModal = ({ isOpen, onClose, onSubmit, productoInitial }: Props) => {
  const form = useForm({
    defaultValues: {
      nombre: productoInitial?.nombre || '',
      descripcion: productoInitial?.descripcion || '',
      precio_base: productoInitial?.precio_base || 0,
      imagen_url: productoInitial?.imagen_url || '',
      disponible: productoInitial?.disponible ?? true,
      categoria_ids: productoInitial?.categoria_ids || [],
    },
    onSubmit: async ({ value }) => {
      const validated = productoFormSchema.parse(value);
      onSubmit(validated as Omit<Producto, 'id'>);
      onClose();
    },
  });

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-md mx-4 max-h-screen overflow-y-auto">
        <h2 className="text-2xl font-bold mb-6">
          {productoInitial ? 'Editar Producto' : 'Nuevo Producto'}
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
                <label className="block text-gray-700 text-sm font-bold mb-2">Nombre</label>
                <input
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
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">Descripción</label>
                <textarea
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

          <form.Field
            name="precio_base"
          >
            {(field) => (
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">Precio Base</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={field.state.value}
                  onChange={(e) => field.handleChange(parseFloat(e.target.value) || 0)}
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
            name="imagen_url"
          >
            {(field) => (
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">URL Imagen (opcional)</label>
                <input
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

          <form.Field name="disponible">
            {(field) => (
              <div className="mb-6">
                <label className="flex items-center text-gray-700 text-sm font-bold">
                  <input
                    type="checkbox"
                    checked={field.state.value}
                    onChange={(e) => field.handleChange(e.target.checked)}
                    onBlur={field.handleBlur}
                    className="mr-2"
                  />
                  Disponible
                </label>
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

export default ProductoModal;
