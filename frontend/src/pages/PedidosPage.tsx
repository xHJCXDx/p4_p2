import { useState, useEffect } from 'react';
import { Pedido } from '../types/pedido';

const API_URL = 'http://localhost:8000/pedidos';

function PedidosPage() {
  const [pedidos, setPedidos] = useState<Pedido[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    usuario_id: 1,
    direccion_id: null as number | null,
    estado_codigo: 'PENDIENTE',
    forma_pago_codigo: 'MERCADOPAGO',
    subtotal: 0,
    descuento: 0,
    costo_envio: 50,
    total: 0,
    notas: '',
  });

  useEffect(() => {
    fetchPedidos();
  }, []);

  const fetchPedidos = async (limit: number = 10, offset: number = 0) => {
    setLoading(true);
    setError(null);
    try {
      const url = new URL(API_URL);
      url.searchParams.append('limit', limit.toString());
      url.searchParams.append('offset', offset.toString());

      const response = await fetch(url.toString());
      const result = await response.json();

      if (result.success && result.data) {
        const items = result.data.items || result.data;
        setPedidos(Array.isArray(items) ? items : []);
      } else {
        setPedidos(result);
      }
    } catch (error) {
      console.error('Error fetching pedidos:', error);
      setError('Error al cargar los pedidos');
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
        await fetchPedidos();
        setIsModalOpen(false);
        resetForm();
      } else {
        setError('Error al crear el pedido');
      }
    } catch (error) {
      console.error('Error creating pedido:', error);
      setError('Error al crear el pedido');
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('¿Estás seguro de eliminar este pedido?')) return;
    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        await fetchPedidos();
      } else {
        setError('Error al eliminar el pedido');
      }
    } catch (error) {
      console.error('Error deleting pedido:', error);
      setError('Error al eliminar el pedido');
    }
  };

  const openCreateModal = () => {
    resetForm();
    setIsModalOpen(true);
  };

  const resetForm = () => {
    setFormData({
      usuario_id: 1,
      direccion_id: null,
      estado_codigo: 'PENDIENTE',
      forma_pago_codigo: 'MERCADOPAGO',
      subtotal: 0,
      descuento: 0,
      costo_envio: 50,
      total: 0,
      notas: '',
    });
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target as HTMLInputElement;
    setFormData({
      ...formData,
      [name]: type === 'number' ? parseFloat(value) : value,
    });
  };

  const getEstadoBadgeColor = (estado: string) => {
    const colors: Record<string, string> = {
      'PENDIENTE': 'bg-yellow-100 text-yellow-800',
      'CONFIRMADO': 'bg-blue-100 text-blue-800',
      'EN_PREP': 'bg-purple-100 text-purple-800',
      'EN_CAMINO': 'bg-orange-100 text-orange-800',
      'ENTREGADO': 'bg-green-100 text-green-800',
      'CANCELADO': 'bg-red-100 text-red-800',
    };
    return colors[estado] || 'bg-gray-100 text-gray-800';
  };

  return (
    <main className="container mx-auto px-4 py-8">
      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800">Pedidos</h2>
        <button
          onClick={openCreateModal}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition-colors shadow-lg"
        >
          + Nuevo Pedido
        </button>
      </div>

      {loading ? (
        <div className="text-center py-8">
          <p className="text-gray-600">Cargando...</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full border-collapse border border-gray-300">
            <thead className="bg-gray-200">
              <tr>
                <th className="border border-gray-300 p-3 text-left">ID</th>
                <th className="border border-gray-300 p-3 text-left">Usuario</th>
                <th className="border border-gray-300 p-3 text-left">Estado</th>
                <th className="border border-gray-300 p-3 text-right">Total</th>
                <th className="border border-gray-300 p-3 text-left">Pago</th>
                <th className="border border-gray-300 p-3 text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {pedidos.map((pedido) => (
                <tr key={pedido.id} className="hover:bg-gray-50">
                  <td className="border border-gray-300 p-3">{pedido.id}</td>
                  <td className="border border-gray-300 p-3">Usuario {pedido.usuario_id}</td>
                  <td className="border border-gray-300 p-3">
<<<<<<< HEAD
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getEstadoBadgeColor(pedido.estado_codigo || '')}`}>
                      {pedido.estado_codigo || 'N/A'}
=======
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getEstadoBadgeColor(pedido.estado_codigo)}`}>
                      {pedido.estado_codigo}
>>>>>>> origin/main
                    </span>
                  </td>
                  <td className="border border-gray-300 p-3 text-right font-bold">${pedido.total?.toFixed(2)}</td>
                  <td className="border border-gray-300 p-3">{pedido.forma_pago_codigo}</td>
                  <td className="border border-gray-300 p-3 text-center">
                    <button
                      onClick={() => handleDelete(pedido.id!)}
                      className="bg-red-600 hover:bg-red-700 text-white font-bold py-1 px-3 rounded text-sm transition-colors"
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {pedidos.length === 0 && (
            <p className="text-center text-gray-600 py-8">No hay pedidos disponibles</p>
          )}
        </div>
      )}

      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-2xl max-w-md w-full">
            <div className="bg-blue-600 text-white p-6">
              <h3 className="text-xl font-bold">Nuevo Pedido</h3>
            </div>
            <form onSubmit={handleCreate} className="p-6 space-y-4">
              <div>
                <label className="block text-gray-700 font-bold mb-2">Usuario ID</label>
                <input
                  type="number"
                  name="usuario_id"
                  value={formData.usuario_id}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700 font-bold mb-2">Subtotal</label>
                <input
                  type="number"
                  name="subtotal"
                  value={formData.subtotal}
                  onChange={handleInputChange}
                  step="0.01"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700 font-bold mb-2">Descuento</label>
                <input
                  type="number"
                  name="descuento"
                  value={formData.descuento}
                  onChange={handleInputChange}
                  step="0.01"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-gray-700 font-bold mb-2">Costo Envío</label>
                <input
                  type="number"
                  name="costo_envio"
                  value={formData.costo_envio}
                  onChange={handleInputChange}
                  step="0.01"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-gray-700 font-bold mb-2">Total</label>
                <input
                  type="number"
                  name="total"
                  value={formData.total}
                  onChange={handleInputChange}
                  step="0.01"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div className="flex gap-2 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition-colors"
                >
                  Crear
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

export default PedidosPage;
