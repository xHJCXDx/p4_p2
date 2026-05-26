import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/useAuthStore';
import { useLogout } from '../hooks/useAuth';

const Navbar = () => {
  const navigate = useNavigate();
  const { usuario, isAuthenticated } = useAuthStore();
  const { mutate: logout } = useLogout();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-blue-600 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-white text-2xl font-bold hover:text-gray-100 transition-colors">
          Admin - Delivery
        </Link>

        <div className="flex gap-6 items-center">
          {isAuthenticated && usuario ? (
            <>
              <span className="text-white text-sm">
                Hola, <span className="font-semibold">{usuario.nombre}</span>
              </span>

              {(() => {
                const isAdmin = usuario.roles.some((r) => r.codigo === 'ADMIN');
                const isStock = usuario.roles.some((r) => r.codigo === 'STOCK');
                const isPedidos = usuario.roles.some((r) => r.codigo === 'PEDIDOS');

                return (
                  <>
                    {(isAdmin) && (
                      <Link
                        to="/categorias"
                        className="text-white hover:text-gray-100 font-semibold transition-colors"
                      >
                        Categorias
                      </Link>
                    )}
                    {(isAdmin || isStock) && (
                      <Link
                        to="/productos"
                        className="text-white hover:text-gray-100 font-semibold transition-colors"
                      >
                        Productos
                      </Link>
                    )}
                    {(isAdmin) && (
                      <Link
                        to="/ingredientes"
                        className="text-white hover:text-gray-100 font-semibold transition-colors"
                      >
                        Ingredientes
                      </Link>
                    )}
                    {(isAdmin || isPedidos) && (
                      <Link
                        to="/cajero"
                        className="text-white hover:text-gray-100 font-semibold transition-colors"
                      >
                        Cajero
                      </Link>
                    )}
                    {(isAdmin || isPedidos) && (
                      <Link
                        to="/pedidos"
                        className="text-white hover:text-gray-100 font-semibold transition-colors"
                      >
                        Pedidos
                      </Link>
                    )}
                  </>
                );
              })()}

              <button
                onClick={handleLogout}
                className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition-colors font-semibold"
              >
                Cerrar sesion
              </button>
            </>
          ) : (
            <Link
              to="/login"
              className="bg-white text-blue-600 px-4 py-2 rounded font-semibold hover:bg-gray-100 transition-colors"
            >
              Iniciar sesion
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
