import { useState } from 'react';
import { useCategorias } from '../../hooks/useCategorias';
import { useProductos } from '../../hooks/useProductos';
import { useCarritoStore } from '../../store/useCarritoStore';

export default function HomeStorePage() {
  const [selectedCategoriaId, setSelectedCategoriaId] = useState<number | undefined>(undefined);
  const [busqueda, setBusqueda] = useState('');
  const { data: categorias = [] } = useCategorias();
  const { data: productos = [] } = useProductos({
    categoria_id: selectedCategoriaId,
    disponible: true,
    busqueda: busqueda || undefined,
  });

  const addItem = useCarritoStore((state) => state.addItem);

  const handleAddToCarrito = (producto: any) => {
    addItem({
      producto_id: producto.id,
      nombre: producto.nombre,
      precio: producto.precio,
      cantidad: 1,
      imagen: producto.imagen,
    });
    alert(`${producto.nombre} agregado al carrito`);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-extrabold text-gray-900 mb-8">Tienda</h1>

        {/* Búsqueda */}
        <div className="mb-8">
          <input
            type="text"
            placeholder="Buscar productos..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Filtro por categoría */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Categorías</h2>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setSelectedCategoriaId(undefined)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedCategoriaId === undefined
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
            >
              Todas
            </button>
            {categorias.map((cat: any) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategoriaId(cat.id)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  selectedCategoriaId === cat.id
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                }`}
              >
                {cat.nombre}
              </button>
            ))}
          </div>
        </div>

        {/* Grilla de productos */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {productos.map((producto: any) => (
            <div key={producto.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
              {producto.imagen && (
                <img src={producto.imagen} alt={producto.nombre} className="w-full h-48 object-cover" />
              )}
              <div className="p-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{producto.nombre}</h3>
                {producto.descripcion && (
                  <p className="text-sm text-gray-600 mb-3">{producto.descripcion}</p>
                )}
                <div className="flex justify-between items-center">
                  <span className="text-2xl font-bold text-blue-600">${producto.precio}</span>
                  <button
                    onClick={() => handleAddToCarrito(producto)}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Agregar
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {productos.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No se encontraron productos</p>
          </div>
        )}
      </div>
    </div>
  );
}
