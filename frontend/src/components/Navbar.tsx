import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/useAuthStore';
import { useLogout } from '../hooks/useAuth';
import { useCarritoStore } from '../store/useCarritoStore';

const Navbar = () => {
  const navigate = useNavigate();
  const { usuario, isAuthenticated } = useAuthStore();
  const { mutate: logout } = useLogout();
  const carrito = useCarritoStore((state) => state.items);

  const handleLogout = () => {
    logout();
    navigate('/admin/login');
  };

  return (
    <nav className="bg-blue-600 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-white text-2xl font-bold hover:text-gray-100 transition-colors">
          Delivery de Alimentos
        </Link>

        <div className="flex gap-6 items-center">
          {isAuthenticated && usuario ? (
            <>
              <span className="text-white text-sm">
                Hola, <span className="font-semibold">{usuario.nombre}</span>
              </span>

              {usuario.roles.some((r) => r.codigo === 'ADMIN') || usuario.roles.some((r) => r.codigo === 'PEDIDOS') ? (
                <>
                  <Link
                    to="/admin/categorias"
                    className="text-white hover:text-gray-100 font-semibold transition-colors"
                  >
                    Categorías
                  </Link>
                  <Link
                    to="/admin/productos"
                    className="text-white hover:text-gray-100 font-semibold transition-colors"
                  >
                    Productos
                  </Link>
                  <Link
                    to="/admin/ingredientes"
                    className="text-white hover:text-gray-100 font-semibold transition-colors"
                  >
                    Ingredientes
                  </Link>
                  <Link
                    to="/admin/cajero"
                    className="text-white hover:text-gray-100 font-semibold transition-colors"
                  >
                    Cajero
                  </Link>
                </>
              ) : (
                <>
                  <Link
                    to="/store/home"
                    className="text-white hover:text-gray-100 font-semibold transition-colors"
                  >
                    Tienda
                  </Link>
                  <Link
                    to="/store/carrito"
                    className="text-white hover:text-gray-100 font-semibold transition-colors relative"
                  >
                    Carrito
                    {carrito.length > 0 && (
                      <span className="absolute top-0 right-0 transform translate-x-2 -translate-y-2 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                        {carrito.length}
                      </span>
                    )}
                  </Link>
                  <Link
                    to="/store/mis-pedidos"
                    className="text-white hover:text-gray-100 font-semibold transition-colors"
                  >
                    Mis Pedidos
                  </Link>
                </>
              )}

              <button
                onClick={handleLogout}
                className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition-colors font-semibold"
              >
                Cerrar sesión
              </button>
            </>
          ) : (
            <>
              <Link
                to="/store/home"
                className="text-white hover:text-gray-100 font-semibold transition-colors"
              >
                Tienda
              </Link>
              <Link
                to="/store/carrito"
                className="text-white hover:text-gray-100 font-semibold transition-colors relative"
              >
                Carrito
                {carrito.length > 0 && (
                  <span className="absolute top-0 right-0 transform translate-x-2 -translate-y-2 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                    {carrito.length}
                  </span>
                )}
              </Link>
              <Link
                to="/admin/login"
                className="bg-white text-blue-600 px-4 py-2 rounded font-semibold hover:bg-gray-100 transition-colors"
              >
                Iniciar sesión
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
