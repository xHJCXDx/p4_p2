import { useState, useEffect } from 'react';
import { Ingrediente } from '../types/ingrediente';

const API_URL = 'http://localhost:8000/ingredientes';

function IngredientesPage() {
  const [ingredientes, setIngredientes] = useState<Ingrediente[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedIngrediente, setSelectedIngrediente] = useState<Ingrediente | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    es_alergeno: false,
  });

  useEffect(() => {
    fetchIngredientes();
  }, []);

  const fetchIngredientes = async (limit: number = 10, offset: number = 0) => {
    setLoading(true);
    setError(null);
    try {
      const url = new URL(API_URL);
      url.searchParams.append('limit', limit.toString());
      url.searchParams.append('offset', offset.toString());

      const response = await fetch(url.toString());
      const result = await response.json();

      // Manejar respuesta estandarizada con paginación
      if (result.success && result.data) {
        const items = result.data.items || result.data;
        setIngredientes(Array.isArray(items) ? items : []);
      } else {
        setIngredientes(result);
      }
    } catch (error) {
      console.error('Error fetching ingredientes:', error);
      setError('Error al cargar los ingredientes');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        await fetchIngredientes();
        setIsModalOpen(false);
        resetForm();
      } else {
        setError('Error al crear el ingrediente');
      }
    } catch (error) {
      console.error('Error creating ingrediente:', error);
      setError('Error al crear el ingrediente');
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedIngrediente) return;

    try {
      const response = await fetch(`${API_URL}/${selectedIngrediente.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        await fetchIngredientes();
        setIsModalOpen(false);
        resetForm();
      } else {
        setError('Error al actualizar el ingrediente');
      }
    } catch (error) {
      console.error('Error updating ingrediente:', error);
      setError('Error al actualizar el ingrediente');
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('¿Estás seguro de eliminar este ingrediente?')) return;
    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        await fetchIngredientes();
      } else {
        setError('Error al eliminar el ingrediente');
      }
    } catch (error) {
      console.error('Error deleting ingrediente:', error);
      setError('Error al eliminar el ingrediente');
    }
  };

  const openCreateModal = () => {
    setSelectedIngrediente(null);
    resetForm();
    setIsModalOpen(true);
  };

  const openEditModal = (ingrediente: Ingrediente) => {
    setSelectedIngrediente(ingrediente);
    setFormData({
      nombre: ingrediente.nombre,
      descripcion: ingrediente.descripcion || '',
      es_alergeno: ingrediente.es_alergeno,
    });
    setIsModalOpen(true);
  };

  const resetForm = () => {
    setFormData({
      nombre: '',
      descripcion: '',
      es_alergeno: false,
    });
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target as HTMLInputElement;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value,
    });
  };

  return (
    <main className="container mx-auto px-4 py-8">
      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800">Ingredientes</h2>
        <button
          onClick={openCreateModal}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition-colors shadow-lg"
        >
          + Nuevo Ingrediente
        </button>
      </div>

      {loading ? (
        <div className="text-center py-8">
          <p className="text-gray-600">Cargando...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {ingredientes.map((ingrediente) => (
            <div key={ingrediente.id} className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-2">{ingrediente.nombre}</h3>
              <p className="text-gray-600 text-sm mb-2">{ingrediente.descripcion || 'Sin descripción'}</p>
              <p className={`text-sm mb-4 ${ingrediente.es_alergeno ? 'text-red-600 font-bold' : 'text-green-600'}`}>
                {ingrediente.es_alergeno ? '⚠️ Es alergeno' : '✓ No es alergeno'}
              </p>
              <div className="flex gap-2">
                <button
                  onClick={() => openEditModal(ingrediente)}
                  className="flex-1 bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-4 rounded-lg transition-colors"
                >
                  Editar
                </button>
                <button
                  onClick={() => handleDelete(ingrediente.id!)}
                  className="flex-1 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg transition-colors"
                >
                  Eliminar
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-2xl max-w-md w-full">
            <div className="bg-blue-600 text-white p-6">
              <h3 className="text-xl font-bold">
                {selectedIngrediente ? 'Editar Ingrediente' : 'Nuevo Ingrediente'}
              </h3>
            </div>
            <form onSubmit={selectedIngrediente ? handleUpdate : handleCreate} className="p-6 space-y-4">
              <div>
                <label className="block text-gray-700 font-bold mb-2">Nombre</label>
                <input
                  type="text"
                  name="nombre"
                  value={formData.nombre}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700 font-bold mb-2">Descripción</label>
                <textarea
                  name="descripcion"
                  value={formData.descripcion}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  name="es_alergeno"
                  checked={formData.es_alergeno}
                  onChange={handleInputChange}
                  className="rounded focus:ring-2 focus:ring-blue-500"
                />
                <label className="ml-2 text-gray-700 font-bold">Es alergeno</label>
              </div>
              <div className="flex gap-2 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition-colors"
                >
                  {selectedIngrediente ? 'Actualizar' : 'Crear'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setIsModalOpen(false);
                    resetForm();
                  }}
                  className="flex-1 bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-lg transition-colors"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}

export default IngredientesPage;
