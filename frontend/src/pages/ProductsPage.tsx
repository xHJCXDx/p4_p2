import { useState } from 'react';
import { ProductoTable } from '../components/ProductoTable';
import ProductoModal from '../components/ProductoModal';
import { Producto } from '../types/producto';
import {
  useProductos,
  useCreateProducto,
  useUpdateProducto,
  useDeleteProducto,
} from '../hooks/useProductos';

function ProductsPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedProducto, setSelectedProducto] = useState<Producto | null>(null);
  const [error, setError] = useState<string | null>(null);

  const { data: productos = [], isLoading } = useProductos();
  const createMutation = useCreateProducto();
  const updateMutation = useUpdateProducto();
  const deleteMutation = useDeleteProducto();

  const handleCreate = async (data: Omit<Producto, 'id'>) => {
    try {
      await createMutation.mutateAsync(data);
      setIsModalOpen(false);
    } catch (err) {
      console.error('Error creating producto:', err);
      setError('Error al crear el producto');
    }
  };

  const handleUpdate = async (data: Omit<Producto, 'id'>) => {
    if (!selectedProducto || !selectedProducto.id) return;
    try {
      await updateMutation.mutateAsync({
        id: selectedProducto.id,
        data: data,
      });
      setIsModalOpen(false);
    } catch (err) {
      console.error('Error updating producto:', err);
      setError('Error al actualizar el producto');
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('¿Estás seguro de eliminar este producto?')) return;
    try {
      await deleteMutation.mutateAsync(id);
    } catch (err) {
      console.error('Error deleting producto:', err);
      setError('Error al eliminar el producto');
    }
  };

  const openCreateModal = () => {
    setSelectedProducto(null);
    setIsModalOpen(true);
  };

  const openEditModal = (producto: Producto) => {
    setSelectedProducto(producto);
    setIsModalOpen(true);
  };

  const handleSubmit = (data: Omit<Producto, 'id'>) => {
    if (selectedProducto) {
      handleUpdate(data);
    } else {
      handleCreate(data);
    }
  };

  return (
    <main className="container mx-auto px-4 py-8">
      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800">Productos</h2>
        <button
          onClick={openCreateModal}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition-colors shadow-lg"
        >
          + Nuevo Producto
        </button>
      </div>

      {isLoading ? (
        <div className="text-center py-8">
          <p className="text-gray-600">Cargando...</p>
        </div>
      ) : (
        <ProductoTable
          data={productos}
          onEdit={openEditModal}
          onDelete={handleDelete}
          isLoading={isLoading}
        />
      )}

      <ProductoModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleSubmit}
        productoInitial={selectedProducto}
      />
    </main>
  );
}

export default ProductsPage;
