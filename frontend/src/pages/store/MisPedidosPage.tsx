import { usePedidos } from '../../hooks/usePedidos';

export default function MisPedidosPage() {
  const { data: pedidos = [], isLoading } = usePedidos();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <p className="text-center text-gray-500">Cargando pedidos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-extrabold text-gray-900 mb-8">Mis Pedidos</h1>

        {pedidos.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No tienes pedidos</p>
          </div>
        ) : (
          <div className="space-y-4">
            {pedidos.map((pedido: any) => (
              <div key={pedido.id} className="bg-white rounded-lg shadow-md p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">Pedido #{pedido.id}</h3>
                    <p className="text-sm text-gray-600">
                      {new Date(pedido.created_at).toLocaleDateString('es-ES')}
                    </p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    pedido.estado_pedido_codigo === 'PENDIENTE'
                      ? 'bg-yellow-100 text-yellow-800'
                      : pedido.estado_pedido_codigo === 'CONFIRMADO'
                      ? 'bg-blue-100 text-blue-800'
                      : pedido.estado_pedido_codigo === 'EN_PREPARACION'
                      ? 'bg-purple-100 text-purple-800'
                      : pedido.estado_pedido_codigo === 'EN_CAMINO'
                      ? 'bg-indigo-100 text-indigo-800'
                      : 'bg-green-100 text-green-800'
                  }`}>
                    {pedido.estado_pedido_codigo}
                  </span>
                </div>

                {pedido.linea_ventas && pedido.linea_ventas.length > 0 && (
                  <div className="mb-4 pb-4 border-b">
                    <p className="text-sm font-medium text-gray-700 mb-2">Productos:</p>
                    <ul className="space-y-1">
                      {pedido.linea_ventas.map((linea: any, idx: number) => (
                        <li key={idx} className="text-sm text-gray-600">
                          • Producto {linea.producto_id} - Cantidad: {linea.cantidad}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-sm text-gray-600">Total:</p>
                    <p className="text-2xl font-bold text-blue-600">${pedido.monto_total.toFixed(2)}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-600">Forma de pago:</p>
                    <p className="text-gray-900 font-medium">{pedido.forma_pago_codigo}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
