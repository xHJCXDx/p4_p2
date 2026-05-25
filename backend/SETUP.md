# 🚀 Setup - Backend P4_P2

Instrucciones para levantar el backend completo con BD seeded.

---

## 📋 Requisitos previos

- Python 3.8+
- pip
- Git (opcional)

---

## 🛠️ Paso 1: Instalar dependencias

```bash
# Navegar al directorio del backend
cd p4_p2/backend

# Crear entorno virtual (opcional pero recomendado)
python -m venv .venv

# Activar el entorno
# En Linux/Mac:
source .venv/bin/activate

# En Windows:
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## 🗄️ Paso 2: Inicializar la BD (IMPORTANTE)

Este paso crea la BD con TODOS los datos necesarios (seed data completo).

```bash
# Ejecutar desde el directorio del backend (p4_p2/backend)
python setup_db.py
```

**Qué hace:**
- Elimina la BD anterior (si existe)
- Crea una BD nueva con todas las tablas
- Seedea:
  - 4 Roles (ADMIN, STOCK, PEDIDOS, CLIENT)
  - 3 Formas de pago (MercadoPago, Efectivo, Transferencia)
  - 6 Estados de pedido (máquina de estados)
  - 1 Usuario admin (admin@admin.com / admin123)
  - 3 Categorías principales + 1 subcategoría
  - 10 Ingredientes (algunos con alergenos)
  - 7 Productos con ingredientes asociados

**Salida esperada:**
```
============================================================
🚀 SETUP DE BASE DE DATOS - Parcial 2
============================================================

🗑️  Eliminando database.db...
✅ Base de datos anterior eliminada

🏗️  Creando tablas...
✅ Tablas creadas

🌱 Seeding roles...
✅ 4 roles seeded

🌱 Seeding catálogos...
✅ Catálogos seeded

🌱 Seeding usuario admin...
✅ Usuario admin creado
   Email: admin@admin.com
   Password: admin123

🌱 Seeding ingredientes...
✅ 10 ingredientes seeded
🌱 Seeding categorías...
✅ 4 categorías seeded
🌱 Seeding productos...
✅ 7 productos seeded
✅ SEED COMPLETO EXITOSO

============================================================
✅ SETUP COMPLETADO EXITOSAMENTE
============================================================

🎉 BD lista para la demo!
   • Admin: admin@admin.com / admin123
   • Categorías: Pizzas, Empanadas, Bebidas
   • Productos: 7 productos con ingredientes
   • Ingredientes: 10 ingredientes (algunos con alergenos)

Para iniciar el servidor:
   fastapi dev main.py
```

---

## 🚀 Paso 3: Iniciar el servidor

```bash
# Desde p4_p2/backend
fastapi dev main.py
```

**Salida esperada:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Press CTRL+C to quit
```

---

## 📡 Verificar que está funcionando

Abre otra terminal y prueba un endpoint:

```bash
# Ver categorías
curl http://localhost:8000/api/v1/categorias

# Ver productos
curl http://localhost:8000/api/v1/productos

# Ver Swagger UI (documentación interactiva)
# Abre en navegador: http://localhost:8000/docs
```

---

## 🔐 Datos de admin

**Credenciales por defecto:**
- Email: `admin@admin.com`
- Password: `admin123`

⚠️ **IMPORTANTE**: Cambiar la contraseña en producción.

---

## 📊 Estructura de la BD

Después de ejecutar `setup_db.py`, tienes:

### **Categorías**
```
├── Pizzas (id: 1)
│   └── Pizzas Dulces (id: 4, parent_id: 1)
├── Empanadas (id: 2)
└── Bebidas (id: 3)
```

### **Ingredientes** (10 total)
- Queso Mozzarella, Tomate, Oregano, Maní, Leche, Huevo, Gluten, Carne molida, Cebolla, Ajo
- Los marcados como alergeno: Maní, Leche, Huevo, Gluten

### **Productos** (7 total)
1. Pizza Margherita - $250
2. Pizza de Carne - $290
3. Empanadas de Carne - $120
4. Empanadas de Queso - $100
5. Coca-Cola 2L - $65
6. Jugo Natural Naranja - $45
7. Pizza de Chocolate - $200

---

## 🔄 Resetear la BD

Si querés volver a empezar:

```bash
python setup_db.py
```

Esto elimina `database.db` y crea una nueva con todos los datos.

---

## 🧪 Para la Demo del Video

Una vez que el servidor está corriendo, podés ejecutar los endpoints:

```bash
# 1. Login como admin
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@admin.com", "password": "admin123"}'

# 2. Ver categorías
curl "http://localhost:8000/api/v1/categorias"

# 3. Ver productos
curl "http://localhost:8000/api/v1/productos"

# 4. Crear un pedido
curl -X POST "http://localhost:8000/api/v1/pedidos" \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": 1,
    "estado_codigo": "PENDIENTE",
    "forma_pago_codigo": "MERCADOPAGO",
    "subtotal": 250.0,
    "descuento": 0.0,
    "costo_envio": 50.0,
    "total": 300.0
  }'

# Ver Swagger UI: http://localhost:8000/docs
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'app'"

**Solución**: Asegúrate de estar en el directorio `p4_p2/backend` cuando ejecutas los comandos.

```bash
cd p4_p2/backend
python setup_db.py
fastapi dev main.py
```

### Error: "database is locked"

**Solución**: FastAPI ya está corriendo en otra terminal. Termina con CTRL+C o abre otra terminal.

### Error: "relation 'usuario' does not exist"

**Solución**: Ejecuta `python setup_db.py` de nuevo. Las tablas no se crearon correctamente.

---

## 📝 Notas importantes

1. **La BD es SQLite** (archivo `database.db` local)
   - No necesita servidor externo
   - Perfecto para desarrollo y demo

2. **Seed data es idempotente**
   - Ejecutar `setup_db.py` múltiples veces no crea duplicados
   - Verifica si cada item ya existe antes de crear

3. **El JWT expira en 30 minutos**
   - Cookie httpOnly, segura

4. **CORS habilitado** para `http://localhost:5173` (frontend Vite)

---

## 🎯 Próximos pasos

1. ✅ Setup BD completado
2. ⏭️ Levantar el frontend (si lo hay)
3. ⏭️ Grabar el video de demostración

---

**¿Dudas?** Revisa los logs del servidor o verifica los endpoints en http://localhost:8000/docs
