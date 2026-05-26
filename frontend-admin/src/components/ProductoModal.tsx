import { useEffect } from 'react';
import { useForm } from '@tanstack/react-form';
import { Producto } from '../types/producto';
import { productoFormSchema } from '../schemas/producto.schema';
import { useCategorias } from '../hooks/useCategorias';
import { useIngredientes } from '../hooks/useIngredientes';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (producto: any) => void;
  productoInitial?: Producto | null;
}

function getDefaults(p?: Producto | null) {
  return {
    nombre: p?.nombre || '',
    descripcion: p?.descripcion || '',
    precio_base: p?.precio_base || 0,
    imagen_url: p?.imagen_url || '',
    stock_cantidad: p?.stock_cantidad || 0,
    disponible: p?.disponible ?? true,
    categoria_ids: p?.categorias?.map((c) => c.id) || [],
    ingrediente_ids: p?.ingredientes?.map((i) => i.id) || [],
  };
}

const ProductoModal = ({ isOpen, onClose, onSubmit, productoInitial }: Props) => {
  const { data: categorias = [] } = useCategorias();
  const { data: ingredientes = [] } = useIngredientes();

  const form = useForm({
    defaultValues: getDefaults(productoInitial),
    onSubmit: async ({ value }) => {
      const validated = productoFormSchema.parse(value);
      onSubmit(validated);
      onClose();
    },
  });

  useEffect(() => {
    if (isOpen) {
      form.reset(getDefaults(productoInitial));
    }
  }, [isOpen, productoInitial]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-lg mx-4 max-h-[90vh] overflow-y-auto">
        <h2 className="text-2xl font-bold mb-6">
          {productoInitial ? 'Editar Producto' : 'Nuevo Producto'}
        </h2>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            form.handleSubmit();
          }}
        >
          <form.Field name="nombre">
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
                  <p key={idx} className="text-red-500 text-xs mt-1">{error}</p>
                ))}
              </div>
            )}
          </form.Field>

          <form.Field name="descripcion">
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
                  <p key={idx} className="text-red-500 text-xs mt-1">{error}</p>
                ))}
              </div>
            )}
          </form.Field>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <form.Field name="precio_base">
              {(field) => (
                <div>
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
                    <p key={idx} className="text-red-500 text-xs mt-1">{error}</p>
                  ))}
                </div>
              )}
            </form.Field>

            <form.Field name="stock_cantidad">
              {(field) => (
                <div>
                  <label className="block text-gray-700 text-sm font-bold mb-2">Stock</label>
                  <input
                    type="number"
                    min="0"
                    value={field.state.value}
                    onChange={(e) => field.handleChange(parseInt(e.target.value) || 0)}
                    onBlur={field.handleBlur}
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  />
                  {field.state.meta.errors.map((error, idx) => (
                    <p key={idx} className="text-red-500 text-xs mt-1">{error}</p>
                  ))}
                </div>
              )}
            </form.Field>
          </div>

          <form.Field name="imagen_url">
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
              </div>
            )}
          </form.Field>

          <form.Field name="disponible">
            {(field) => (
              <div className="mb-4">
                <label className="flex items-center text-gray-700 text-sm font-bold">
                  <input
                    type="checkbox"
                    checked={field.state.value}
                    onChange={(e) => field.handleChange(e.target.checked)}
                    className="mr-2"
                  />
                  Disponible
                </label>
              </div>
            )}
          </form.Field>

          <form.Field name="categoria_ids">
            {(field) => (
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">Categorías</label>
                <div className="border rounded p-3 max-h-40 overflow-y-auto bg-gray-50">
                  {categorias.length === 0 ? (
                    <p className="text-gray-400 text-sm">No hay categorías disponibles</p>
                  ) : (
                    categorias.map((cat) => (
                      <label key={cat.id} className="flex items-center mb-1 text-sm">
                        <input
                          type="checkbox"
                          checked={field.state.value.includes(cat.id!)}
                          onChange={(e) => {
                            const current = field.state.value;
                            if (e.target.checked) {
                              field.handleChange([...current, cat.id!]);
                            } else {
                              field.handleChange(current.filter((id) => id !== cat.id));
                            }
                          }}
                          className="mr-2"
                        />
                        {cat.nombre}
                      </label>
                    ))
                  )}
                </div>
              </div>
            )}
          </form.Field>

          <form.Field name="ingrediente_ids">
            {(field) => (
              <div className="mb-6">
                <label className="block text-gray-700 text-sm font-bold mb-2">Ingredientes</label>
                <div className="border rounded p-3 max-h-40 overflow-y-auto bg-gray-50">
                  {ingredientes.length === 0 ? (
                    <p className="text-gray-400 text-sm">No hay ingredientes disponibles</p>
                  ) : (
                    ingredientes.map((ing) => (
                      <label key={ing.id} className="flex items-center mb-1 text-sm">
                        <input
                          type="checkbox"
                          checked={field.state.value.includes(ing.id!)}
                          onChange={(e) => {
                            const current = field.state.value;
                            if (e.target.checked) {
                              field.handleChange([...current, ing.id!]);
                            } else {
                              field.handleChange(current.filter((id) => id !== ing.id));
                            }
                          }}
                          className="mr-2"
                        />
                        {ing.nombre}
                        {ing.es_alergeno && (
                          <span className="ml-2 text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full">
                            Alérgeno
                          </span>
                        )}
                      </label>
                    ))
                  )}
                </div>
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
