import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import { ProtectedRoute } from './components/ProtectedRoute';

// Admin pages
import LoginPage from './pages/admin/LoginPage';
import CajeroPage from './pages/admin/CajeroPage';

// Store pages
import HomeStorePage from './pages/store/HomeStorePage';
import CarritoPage from './pages/store/CarritoPage';
import CheckoutPage from './pages/store/CheckoutPage';
import MisPedidosPage from './pages/store/MisPedidosPage';

// Legacy admin pages (CRUD)
import CategoriasPage from './pages/CategoriasPage';
import ProductsPage from './pages/ProductsPage';
import IngredientesPageRefactored from './pages/IngredientesPageRefactored';
import PedidosPageRefactored from './pages/PedidosPageRefactored';

// Error pages
const NotFoundPage = () => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">404</h1>
      <p className="text-gray-600 mb-4">Página no encontrada</p>
    </div>
  </div>
);

const ForbiddenPage = () => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">403</h1>
      <p className="text-gray-600 mb-4">No tienes permiso para acceder a este recurso</p>
    </div>
  </div>
);

function AppRoutes() {
  return (
    <Routes>
      {/* Auth */}
      <Route path="/admin/login" element={<LoginPage />} />

      {/* Admin routes */}
      <Route
        path="/admin"
        element={
          <ProtectedRoute roles={['ADMIN', 'PEDIDOS', 'STOCK']}>
            <Navigate to="/admin/cajero" replace />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/cajero"
        element={
          <ProtectedRoute roles={['ADMIN', 'PEDIDOS']}>
            <CajeroPage />
          </ProtectedRoute>
        }
      />

      {/* Legacy admin pages - CRUD operations */}
      <Route
        path="/admin/categorias"
        element={
          <ProtectedRoute roles={['ADMIN']}>
            <CategoriasPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/productos"
        element={
          <ProtectedRoute roles={['ADMIN', 'STOCK']}>
            <ProductsPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/ingredientes"
        element={
          <ProtectedRoute roles={['ADMIN']}>
            <IngredientesPageRefactored />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/pedidos"
        element={
          <ProtectedRoute roles={['ADMIN', 'PEDIDOS']}>
            <PedidosPageRefactored />
          </ProtectedRoute>
        }
      />

      {/* Store routes */}
      <Route path="/store/home" element={<HomeStorePage />} />
      <Route path="/store/carrito" element={<CarritoPage />} />
      <Route
        path="/store/checkout"
        element={
          <ProtectedRoute roles={['CLIENT']}>
            <CheckoutPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/store/mis-pedidos"
        element={
          <ProtectedRoute roles={['CLIENT']}>
            <MisPedidosPage />
          </ProtectedRoute>
        }
      />

      {/* Error pages */}
      <Route path="/403" element={<ForbiddenPage />} />
      <Route path="/404" element={<NotFoundPage />} />

      {/* Default redirect */}
      <Route path="/" element={<Navigate to="/store/home" replace />} />
      <Route path="*" element={<Navigate to="/404" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <AppRoutes />
      </div>
    </Router>
  );
}

export default App;
