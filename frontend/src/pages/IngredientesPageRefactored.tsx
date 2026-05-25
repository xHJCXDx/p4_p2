import { useState, useEffect } from 'react';
import { Ingrediente } from '../types/ingrediente';
import { IngredienteFormSimple } from '../components/IngredienteFormSimple';
import { IngredienteTable } from '../components/IngredienteTable';
import {
  useIngredientes,
  useCreateIngrediente,
  useUpdateIngrediente,
  useDeleteIngrediente,
} from '../hooks/useIngredientes';

function IngredientesPageRefactored() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedIngrediente, setSelectedIngrediente] = useState<Ingrediente | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const { data: ingredientes = [], isLoading } = useIngredientes();
  const createMutation = useCreateIngrediente();
  const updateMutation = useUpdateIngrediente();
  const deleteMutation = useDeleteIngrediente();

  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  const handleFormSubmit = async (data: Omit<Ingrediente, 'id' | 'created_at' | 'updated_at'>) => {
    try {
      if (selectedIngrediente && selectedIngrediente.id) {
        await updateMutation.mutateAsync({
          id: selectedIngrediente.id,
          data,
        });
        setSuccessMessage('Ingrediente actualizado exitosamente');
      } else {
        await createMutation.mutateAsync(data);
        setSuccessMessage('Ingrediente creado exitosamente');
      }
      setIsModalOpen(false);
      setSelectedIngrediente(null);
    } catch (err) {
      console.error('Error:', err);
      setError(`Error al ${selectedIngrediente ? 'actualizar' : 'crear'} el ingrediente`);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('¿Estás seguro de eliminar este ingrediente?')) return;

    try {
      await deleteMutation.mutateAsync(id);
      setSuccessMessage('Ingrediente eliminado exitosamente');
    } catch (err) {
      console.error('Error deleting:', err);
      setError('Error al eliminar el ingrediente');
    }
  };

  const openCreateModal = () => {
    setSelectedIngrediente(null);
    setIsModalOpen(true);
  };

  const openEditModal = (ingrediente: Ingrediente) => {
    setSelectedIngrediente(ingrediente);
    setIsModalOpen(true);
  };

  return (
    <main className="container mx-auto px-4 py-8">
      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg flex justify-between items-center">
          <span>{error}</span>
          <button onClick={() => setError(null)} className="text-red-700 hover:text-red-900">
            ✕
          </button>
        </div>
      )}

      {successMessage && (
        <div className="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg flex justify-between items-center">
          <span>{successMessage}</span>
          <button onClick={() => setSuccessMessage(null)} className="text-green-700 hover:text-green-900">
            ✕
          </button>
        </div>
      )}

      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800">Ingredientes</h2>
        <button
          onClick={openCreateModal}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition-colors shadow-lg"
        >
          + Nuevo Ingrediente
        </button>
      </div>

      {/* Tabla */}
      <IngredienteTable
        data={ingredientes}
        onEdit={openEditModal}
        onDelete={handleDelete}
        isLoading={isLoading}
      />

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-2xl max-w-md w-full">
            <div className="bg-blue-600 text-white p-6">
              <h3 className="text-xl font-bold">
                {selectedIngrediente ? 'Editar Ingrediente' : 'Nuevo Ingrediente'}
              </h3>
            </div>
            <div className="p-6">
              <IngredienteFormSimple
                onSubmit={handleFormSubmit}
                onCancel={() => {
                  setIsModalOpen(false);
                  setSelectedIngrediente(null);
                }}
                initialData={selectedIngrediente || undefined}
                isLoading={createMutation.isPending || updateMutation.isPending}
              />
            </div>
          </div>
        </div>
      )}
    </main>
  );
}

export default IngredientesPageRefactored;
