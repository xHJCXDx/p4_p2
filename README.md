# Parcial 2 - Programación IV (UTN)

**Autores**: Hiro Cruz, Mauricio Manzano  
**Proyecto**: Tienda de Alimentos - Full Stack

## Descripción General

**Parcial 2** es una evolución significativa del TP Integrador (P4_P1), ampliando la arquitectura con autenticación, autorización, gestión de pedidos y una tienda pública funcional.

## Novedades en Parcial 2 vs TP Integrador (P4_P1)

Parcial 2 amplía significativamente la funcionalidad del TP Integrador:

- **Autenticación y Autorización**: Sistema JWT con roles RBAC (ADMIN, GERENTE, REPARTIDOR, CLIENTE)
- **Gestión de Pedidos**: Máquina de estados validada, detalles de compra con snapshots, historial de transiciones
- **Módulos Nuevos**: Usuarios, Direcciones, Ingredientes, Panel Administrativo
- **Tienda Pública**: Catálogo de productos, carrito, checkout y historial de pedidos del cliente
- **Mejoras Backend**: Unit of Work Pattern, Repository Pattern, API versionada (`/api/v1/`)
- **Mejoras Frontend**: React Router protegido, State Management con Zustand, TanStack Query para servidor
- **Base de Datos**: PostgreSQL con soft deletes, auditoría automática y relaciones complejas

## Proyecto Full Stack: React + TypeScript + FastAPI

## Requisitos Previos

- Python 3.8+
- Node.js 18+
- npm

## Estructura del Proyecto - Parcial 2

```
p4_p2/
├── backend/          # API FastAPI con autenticación y autorización
│   ├── app/
│   │   ├── core/                    # Configuración central
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   ├── constants.py
│   │   │   ├── response.py
│   │   │   ├── repository.py
│   │   │   └── unit_of_work.py
│   │   │
│   │   ├── usuario/                 # Autenticación (NUEVO)
│   │   │   ├── model.py
│   │   │   ├── schema.py
│   │   │   ├── service.py
│   │   │   ├── repository.py
│   │   │   └── router.py
│   │   │
│   │   ├── categoria/
│   │   ├── producto/
│   │   ├── ingrediente/             # (NUEVO)
│   │   ├── pedido/                  # (NUEVO)
│   │   ├── direccion/               # (NUEVO)
│   │   ├── catalogo/                # (NUEVO)
│   │   ├── admin/                   # (NUEVO)
│   │   ├── seed.py
│   │   └── main.py
│   │
│   ├── database.db
│   ├── requirements.txt
│   └── api.http
│
└── frontend/         # React + TypeScript + Vite
    ├── src/
    │   ├── api/                     # Axios config (NUEVO)
    │   ├── components/
    │   ├── hooks/                   # Custom hooks (NUEVO)
    │   ├── pages/
    │   ├── store/                   # Zustand stores (NUEVO)
    │   ├── types/
    │   ├── App.tsx
    │   └── main.tsx
    │
    ├── package.json
    ├── vite.config.ts
    └── tailwind.config.ts
```

## Instalación y Ejecución

### Backend

```bash
cd backend

# Crear y activar entorno virtual
python -m venv .venv

# En macOS/Linux:
source .venv/bin/activate

# En Windows:
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
fastapi dev main.py
```

El servidor estará disponible en `http://localhost:8000`
- Documentación interactiva: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

---

## Modelo de Datos (Conforme ERD - Dominio 2)

### **Tabla: Producto**
- `id` (BIGINT, PK)
- `nombre` (VARCHAR(150), NN, Indexed)
- `descripcion` (TEXT)
- `precio_base` (DECIMAL(10,2), NN, CHECK >= 0)
- `imagenes_url` (JSON Array)
- `stock_cantidad` (INTEGER, NN, DEFAULT 0, CHECK >= 0)
- `disponible` (BOOLEAN, NN, DEFAULT true)
- `created_at` (TIMESTAMPTZ, NN)
- `updated_at` (TIMESTAMPTZ, NN)
- `deleted_at` (TIMESTAMPTZ, nullable) ← Soft Delete

### **Tabla: Categoria**
- `id` (BIGINT, PK)
- `parent_id` (BIGINT, FK -> Categoria.id, nullable) ← Jerarquía/Auto-referencia
- `nombre` (VARCHAR(100), NN, UNIQUE)
- `descripcion` (TEXT)
- `imagen_url` (TEXT, nullable)
- `created_at` (TIMESTAMPTZ, NN)
- `updated_at` (TIMESTAMPTZ, NN)
- `deleted_at` (TIMESTAMPTZ, nullable) ← Soft Delete

### **Tabla: Ingrediente**
- `id` (BIGINT, PK)
- `nombre` (VARCHAR(100), NN, UNIQUE, Indexed)
- `descripcion` (TEXT)
- `es_alergeno` (BOOLEAN, NN, DEFAULT false)
- `created_at` (TIMESTAMPTZ, NN)
- `updated_at` (TIMESTAMPTZ, NN)

### **Tabla: ProductoCategoria** (Many-to-Many)
- `producto_id` (BIGINT, PK, FK -> Producto.id)
- `categoria_id` (BIGINT, PK, FK -> Categoria.id)
- `es_principal` (BOOLEAN, NN, DEFAULT false)
- `created_at` (TIMESTAMPTZ, NN)

### **Tabla: ProductoIngrediente** (Many-to-Many)
- `producto_id` (BIGINT, PK, FK -> Producto.id)
- `ingrediente_id` (BIGINT, PK, FK -> Ingrediente.id)
- `es_removible` (BOOLEAN, NN, DEFAULT false)

---

## Características Implementadas

### Backend (FastAPI) - Parcial 2

#### Autenticación y Autorización
- **JWT Token-based Auth**
  - `POST /api/v1/auth/register` - Registrar nuevo usuario
  - `POST /api/v1/auth/login` - Login (retorna access_token)
  - `POST /api/v1/auth/refresh` - Refrescar token expirado
  - `POST /api/v1/auth/logout` - Logout (invalida token)

- **RBAC (Role-Based Access Control)**
  - Roles: ADMIN, GERENTE, REPARTIDOR, CLIENTE
  - Seed automático de roles obligatorios
  - Usuario ADMIN por defecto (admin@admin.com / admin123)
  - Decoradores: `@require_auth`, `@require_role("ADMIN")`

#### CRUD Categorías (Parcial 1 + mejoras)
- `GET /api/v1/categorias?limit=10&offset=0` - Listar con paginación
- `GET /api/v1/categorias/{id}` - Obtener por ID
- `POST /api/v1/categorias` - Crear nueva (solo ADMIN)
- `PUT /api/v1/categorias/{id}` - Actualizar (solo ADMIN)
- `DELETE /api/v1/categorias/{id}` - Soft delete (solo ADMIN)
- **Nuevo**: Auto-referencia con `parent_id` (subcategorías)

#### CRUD Productos (Parcial 1 + mejoras)
- `GET /api/v1/productos?limit=10&offset=0` - Listar con paginación, filtros
- `GET /api/v1/productos/{id}` - Obtener por ID
- `POST /api/v1/productos` - Crear nuevo (solo ADMIN)
- `PUT /api/v1/productos/{id}` - Actualizar (solo ADMIN)
- `DELETE /api/v1/productos/{id}` - Soft delete (solo ADMIN)
- **Nuevo**: Relaciones Many-to-Many con Ingredientes

#### CRUD Ingredientes (Nuevo en Parcial 2)
- `GET /api/v1/ingredientes?limit=10&offset=0` - Listar con paginación
- `GET /api/v1/ingredientes/{id}` - Obtener por ID
- `POST /api/v1/ingredientes` - Crear nuevo (solo ADMIN)
- `PUT /api/v1/ingredientes/{id}` - Actualizar (solo ADMIN)
- `DELETE /api/v1/ingredientes/{id}` - Hard delete (sin soft delete)
- **Soporte**: Campo `es_alergeno` para alertas

#### CRUD Pedidos (Nuevo en Parcial 2)
- `GET /api/v1/pedidos?limit=10&offset=0` - Listar con paginación
- `GET /api/v1/pedidos/{id}` - Obtener por ID con detalles completos
- `POST /api/v1/pedidos` - Crear nuevo pedido (solo CLIENTE)
- `PUT /api/v1/pedidos/{id}` - Actualizar pedido (notas, costo_envio)
- `DELETE /api/v1/pedidos/{id}` - Soft delete (solo ADMIN)
- `POST /api/v1/pedidos/{id}/transition-estado` - Cambiar estado (FSM validado)
- `GET /api/v1/pedidos/{id}/detalles` - Obtener detalles (con snapshots)
- `POST /api/v1/pedidos/{id}/detalles` - Agregar detalle a pedido
- `GET /api/v1/pedidos/{id}/pagos` - Obtener pagos realizados
- `POST /api/v1/pedidos/{id}/pagos` - Registrar pago (MercadoPago)
- `PUT /api/v1/pedidos/{id}/pagos/{pago_id}` - Actualizar pago

#### CRUD Direcciones (Nuevo en Parcial 2)
- `GET /api/v1/usuarios/{usuario_id}/direcciones` - Listar direcciones del usuario
- `POST /api/v1/usuarios/{usuario_id}/direcciones` - Crear nueva dirección
- `PUT /api/v1/direcciones/{id}` - Actualizar dirección
- `DELETE /api/v1/direcciones/{id}` - Eliminar dirección
- **Validación**: Calle, número, departamento, ciudad, código postal, provincia

#### Admin Panel (Nuevo en Parcial 2)
- `GET /api/v1/admin/estadisticas` - Estadísticas globales (solo ADMIN)
- `GET /api/v1/admin/usuarios` - Listar todos los usuarios (solo ADMIN)
- `PUT /api/v1/admin/usuarios/{id}/roles` - Asignar/remover roles (solo ADMIN)
- `GET /api/v1/admin/pedidos` - Ver todos los pedidos sin filtro (solo ADMIN)

#### Catálogos (Nuevo en Parcial 2)
- **FormaPago**: MERCADOPAGO, EFECTIVO, TRANSFERENCIA
- **EstadoPedido**: PENDIENTE, CONFIRMADO, EN_PREP, EN_CAMINO, ENTREGADO, CANCELADO
- **Estados**: Seed automático al iniciar la aplicación

#### Características Técnicas
- **Paginación**: Query params `limit` (1-100, default 10) y `offset` (default 0)
- **Respuestas estandarizadas**: `{ success, message, data, status_code }`
- **Soft Delete**: Registros marcados con `deleted_at` (excepto Ingredientes)
- **Auditoría**: `created_at`, `updated_at`, `deleted_at` en todas las tablas
- **Relaciones**: Many-to-Many (Producto-Categoría, Producto-Ingrediente), Auto-referencia (Categoría)
- **CORS**: Configurado para localhost:5173
- **Docs automáticos**: Swagger en `/api/v1/docs`
- **FSM**: Validación automática de transiciones de estado en Pedidos
- **Snapshots**: Copias immutables de precio/nombre en DetallePedido
- **Unit of Work**: Transacciones atómicas con context manager
- **Repository Pattern**: Abstracción de acceso a datos
- **Prefijo API**: `/api/v1/` para versionamiento

### Frontend (React + TypeScript) - Parcial 2

#### Routing con React Router v6
- **Rutas Públicas**:
  - `/` - Redirige a `/store/home`
  - `/store/home` - Catálogo de productos (HomeStorePage)
  - `/store/carrito` - Carrito de compras (CarritoPage)
  - `/store/checkout` - Flujo de compra (CheckoutPage)

- **Rutas Protegidas (CLIENTE)**:
  - `/store/mis-pedidos` - Historial de pedidos del usuario (MisPedidosPage)

- **Rutas de Administración** (solo ADMIN):
  - `/admin/categorias` - Gestión de categorías
  - `/admin/productos` - Gestión de productos
  - `/admin/ingredientes` - Gestión de ingredientes
  - `/admin/pedidos` - Ver todos los pedidos

- **Rutas de Auth**:
  - `/auth/login` - Formulario de login
  - `/auth/register` - Formulario de registro

#### Tienda Pública (Nuevo en Parcial 2)
- **HomeStorePage**
  - Catálogo responsivo de productos
  - Filtros por categoría
  - Búsqueda por nombre/descripción
  - Cards con imagen, precio, descripción
  - Botón "Agregar al carrito"
  - Paginación

- **CarritoPage**
  - Tabla de items en carrito
  - Cantidad ajustable por item
  - Subtotal por item y total general
  - Botón "Proceder al checkout"
  - Carrito vacío - redirige a HomeStorePage

- **CheckoutPage**
  - Resumen de compra
  - Selección de dirección de entrega
  - Selección de forma de pago
  - Botón "Confirmar pedido"
  - Confirmación de pedido creado

- **MisPedidosPage**
  - Tabla de pedidos del usuario
  - Estados con badges (colores distintivos)
  - Detalles expandibles (ej: productos en pedido)
  - Filtros por estado
  - Paginación

#### Panel Administrativo (Nuevo en Parcial 2)
**Gestión de Categorías (CategoriasPage)**
- CRUD completo (Create, Read, Update, Delete)
- Modal para crear/editar
- Tabla responsiva con acciones
- Soporte para subcategorías (parent_id)

**Gestión de Productos (ProductsPage)**
- CRUD completo con modal
- Grid/tabla responsiva
- Campos: nombre, descripción, precio, stock, disponibilidad
- Soporte para múltiples imágenes (array)
- Asociación con ingredientes

**Gestión de Ingredientes (IngredientesPage)**
- CRUD completo
- Indicadores visuales para alergenos
- Tabla con propiedades

**PedidosPageRefactored**
- Vista de todos los pedidos (solo ADMIN)
- Estados con badges
- Información: usuario, estado, total, forma de pago, fecha
- Detalles del pedido (productos + precios)
- Manejo de paginación

#### Autenticación y Protección (Nuevo en Parcial 2)
- **Auth Store (Zustand)**
  - `useAuthStore`: Estado global de autenticación
  - Token JWT almacenado en localStorage
  - Usuario logueado con rol asociado
  - Funciones: login, logout, register

- **ProtectedRoute**
  - Componente que valida autenticación
  - Redirige a /auth/login si no está autenticado
  - Valida roles si es necesario

- **Navbar Actualizado**
  - Links dinámicos según autenticación
  - Mostrar usuario logueado
  - Botón logout
  - Links a admin si es ADMIN
  - Estilos hover y animaciones

#### State Management (Zustand)
- **useCarritoStore**: Gestión del carrito
  - Agregar/remover items
  - Actualizar cantidades
  - Calcular total
  - Limpiar carrito después de checkout

- **useAuthStore**: Gestión de autenticación
  - Token y usuario actual
  - Login/logout/register
  - Validar autenticación

#### Custom Hooks (Nuevo en Parcial 2)
- `useCategorias`: Cargar categorías con paginación
- `useProductos`: Cargar productos con filtros
- `useIngredientes`: Cargar ingredientes
- `usePedidos`: Cargar pedidos del usuario

#### Componentes Reutilizables
- **Navbar**: Navegación principal con links dinámicos
- **CategoriaCard**: Card de categoría
- **ProductoTable/ProductoModal**: CRUD de productos
- **IngredienteTable/IngredienteFormSimple**: CRUD de ingredientes
- **PedidoTable/PedidoFormSimple**: CRUD de pedidos
- **ProtectedRoute**: Protección de rutas por auth + rol
- **Modales genéricos**: Para crear/editar items

#### Diseño con Tailwind CSS
- Componentes responsivos (mobile-first)
- Tema profesional blue/gray
- Validación en formularios
- Indicadores de loading
- Mensajes de error/éxito
- Animations y transitions suaves

---

## Estructura de Respuestas

### Respuesta exitosa con paginación:
```json
{
  "success": true,
  "message": "Categorías obtenidas exitosamente",
  "data": {
    "items": [...],
    "total": 15,
    "limit": 10,
    "offset": 0
  },
  "status_code": 200
}
```

### Respuesta de error:
```json
{
  "success": false,
  "message": "Categoría no encontrada",
  "data": null,
  "status_code": 404
}
```

---

## Pruebas de la API

Usa el archivo `backend/api.http` para probar los endpoints con:
- **Visual Studio Code**: Extensión "REST Client" (REST Client Extension)
- **Postman**: Importar y ejecutar
- **Insomnia**: Importar y ejecutar

Incluye ejemplos de:
- CRUD de Categorías (con parent_id para subcategorías)
- CRUD de Productos (con imagenes_url array y stock_cantidad)
- Paginación (limit y offset)
- Soft deletes

---

## Notas Importantes

### Base de Datos
- SQLite en memoria (desarrollo)
- Fácilmente configurable a PostgreSQL en `app/core/database.py`

### Frontend
- Conecta automáticamente a `http://localhost:8000`
- Manejo de respuestas estandarizadas con paginación
- HMR (Hot Module Reload) habilitado con Vite

### Backend
- FastAPI dev mode con auto-reload
- Validación con Pydantic
- Documentación automática en `/docs`

### Auditoría y Soft Deletes
- Los registros **nunca se borran físicamente**
- El campo `deleted_at` marca la eliminación lógica
- Todas las queries filtran automáticamente `deleted_at IS NULL`
- Útil para reportes y auditoría

### Jerarquía de Categorías
- Campo `parent_id` permite categorías padre/hijas
- Auto-referencia en la tabla Categoria
- Ejemplo: "Alimentos" (padre) -> "Bebidas" (hija)

---

## Comparativa: TP Integrador (P4_P1) vs Parcial 2 (P4_P2)

| Feature | P4_P1 (TP Integrador) | P4_P2 (Parcial 2) |
|---------|----------------------|-------------------|
| **Autenticación** | No | Yes - JWT + RBAC |
| **Usuarios y Roles** | No | Yes - ADMIN, GERENTE, REPARTIDOR, CLIENTE |
| **Categorías** | Yes - CRUD básico | Yes - CRUD + Jerarquía (parent_id) |
| **Productos** | Yes - CRUD básico | Yes - CRUD + Relaciones M2M |
| **Ingredientes** | No | Yes - CRUD + Alergenos |
| **Pedidos** | No | Yes - CRUD + FSM + Snapshots + Pagos |
| **Direcciones** | No | Yes - CRUD + Validación |
| **Admin Panel** | No | Yes - Estadísticas + Gestión global |
| **Tienda Pública** | No | Yes - HomeStore + Carrito + Checkout |
| **State Management** | No | Yes - Zustand (Auth + Carrito) |
| **Custom Hooks** | No | Yes - useCategorias, useProductos, etc. |
| **ProtectedRoute** | No | Yes - Validación Auth + Rol |
| **Frontend Routing** | Básico | Yes - React Router v6 con guards |
| **API Versionamiento** | `/categorias` | Yes - `/api/v1/categorias` |
| **Unit of Work** | No | Yes - Context manager |
| **Repository Pattern** | No | Yes - BaseRepository genérico |
| **Soft Deletes** | Yes | Yes (mejorado) |
| **Response Envelope** | Yes - Básico | Yes - StandardResponse mejorado |
| **Frontend Build** | No (manual) | Yes - Vite + HMR |
| **Tailwind CSS** | No | Yes (diseño responsivo) |

---

## Stack Tecnológico

| Capa | Tecnología | Versión |
|------|-----------|---------|
| **Backend** | FastAPI | 0.100+ |
| **BD** | SQLModel / SQLAlchemy | 2.0+ |
| **Auth** | PyJWT | 2.8+ |
| **Password Hash** | Passlib + bcrypt | — |
| **Frontend** | React | 18.2+ |
| **Router** | React Router | 6.20+ |
| **State** | Zustand | 4.4+ |
| **Tipos** | TypeScript | 5.2+ |
| **Estilos** | Tailwind CSS | 3.4+ |
| **HTTP Client** | Axios | 1.6+ |
| **Build** | Vite | 5.0+ |

---

## Comparativa: Requisitos Entregables

### TP Integrador (P4_P1)
- Categorías CRUD
- Productos CRUD
- Relación Producto-Categoría (M2M)
- SQLModel + SQLAlchemy
- FastAPI con documentación automática
- Paginación en listados
- Validación con Pydantic

### Parcial 2 (P4_P2) - Todos los de P4_P1 PLUS:
- **Autenticación JWT**
- **RBAC con roles**
- **Módulo Usuarios**
- **Módulo Ingredientes**
- **Módulo Pedidos con FSM**
- **Módulo Direcciones**
- **Pedidos con Detalles + Snapshots**
- **Sistema de Pagos (estructura)**
- **Panel Administrativo**
- **Tienda Pública (HomeStore + Carrito + Checkout)**
- **MisPedidos (historial de usuario)**
- **Frontend React + TypeScript + Vite**
- **State Management (Zustand)**
- **Routing protegido (ProtectedRoute)**
- **Unit of Work Pattern**
- **Repository Pattern**
- **API Versionamiento (/api/v1/)**
- **Tailwind CSS**
- **Refactoring de routers** (limpieza de código)

