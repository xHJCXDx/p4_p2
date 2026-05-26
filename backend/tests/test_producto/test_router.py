"""Tests para los routers de productos."""

import pytest
from app.producto.schema import ProductoCreate
from app.categoria.schema import CategoriaCreate
from app.producto import service as producto_service
from app.categoria import service as categoria_service


def test_get_productos_sin_datos(client):
    """GET / sin productos debe retornar lista vacía."""
    response = client.get("/api/v1/productos/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total"] == 0
    assert len(data["data"]["items"]) == 0


def test_get_productos_con_datos(client, session):
    """GET / con productos creados."""
    # Crear 4 productos
    for i in range(4):
        prod_data = ProductoCreate(
            nombre=f"Producto {i}",
            descripcion=f"Descripción {i}",
            precio_base=100.0 * (i + 1)
        )
        producto_service.create(session, prod_data)

    response = client.get("/api/v1/productos/")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total"] == 4
    assert len(data["data"]["items"]) == 4


def test_get_productos_paginacion(client, session):
    """GET / respeta limit y offset."""
    for i in range(6):
        prod_data = ProductoCreate(
            nombre=f"Prod {i}",
            descripcion=f"Desc {i}",
            precio_base=100.0
        )
        producto_service.create(session, prod_data)

    # Primera página: limit=3
    response = client.get("/api/v1/productos/?limit=3&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["items"]) == 3
    assert data["data"]["total"] == 6

    # Segunda página
    response = client.get("/api/v1/productos/?limit=3&offset=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["items"]) == 3


def test_get_productos_filtro_disponible(client, session):
    """GET / con filtro disponible."""
    # Crear 2 disponibles y 1 no disponible
    prod_data1 = ProductoCreate(nombre="Disponible 1", descripcion="", precio_base=100.0, disponible=True)
    producto_service.create(session, prod_data1)

    prod_data2 = ProductoCreate(nombre="No disponible", descripcion="", precio_base=100.0, disponible=False)
    producto_service.create(session, prod_data2)

    prod_data3 = ProductoCreate(nombre="Disponible 2", descripcion="", precio_base=100.0, disponible=True)
    producto_service.create(session, prod_data3)

    # Filtrar solo disponibles
    response = client.get("/api/v1/productos/?disponible=true")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total"] == 2

    # Filtrar solo no disponibles
    response = client.get("/api/v1/productos/?disponible=false")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total"] == 1


def test_get_productos_filtro_busqueda(client, session):
    """GET / con filtro de búsqueda por nombre."""
    prod1 = ProductoCreate(nombre="Hamburguesa", descripcion="", precio_base=100.0)
    producto_service.create(session, prod1)

    prod2 = ProductoCreate(nombre="Hamburguesón", descripcion="", precio_base=100.0)
    producto_service.create(session, prod2)

    prod3 = ProductoCreate(nombre="Pizza", descripcion="", precio_base=100.0)
    producto_service.create(session, prod3)

    # Buscar "hamb"
    response = client.get("/api/v1/productos/?busqueda=hamb")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total"] == 2

    # Buscar "pizza"
    response = client.get("/api/v1/productos/?busqueda=pizza")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total"] == 1


def test_get_productos_filtro_categoria(client, session):
    """GET / con filtro por categoría."""
    # Crear categorías
    cat1_data = CategoriaCreate(nombre="Comidas", descripcion="")
    cat1 = categoria_service.create(session, cat1_data)
    session.refresh(cat1)

    cat2_data = CategoriaCreate(nombre="Bebidas", descripcion="")
    cat2 = categoria_service.create(session, cat2_data)
    session.refresh(cat2)

    # Crear productos: 2 en cat1, 1 en cat2
    prod1 = ProductoCreate(nombre="Hamburguesa", descripcion="", precio_base=100.0, categoria_ids=[cat1.id])
    producto_service.create(session, prod1)

    prod2 = ProductoCreate(nombre="Pizza", descripcion="", precio_base=100.0, categoria_ids=[cat1.id])
    producto_service.create(session, prod2)

    prod3 = ProductoCreate(nombre="Coca Cola", descripcion="", precio_base=50.0, categoria_ids=[cat2.id])
    producto_service.create(session, prod3)

    # Filtrar por cat1
    response = client.get(f"/api/v1/productos/?categoria_id={cat1.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total"] == 2

    # Filtrar por cat2
    response = client.get(f"/api/v1/productos/?categoria_id={cat2.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total"] == 1


def test_create_producto_sin_auth(client):
    """POST / sin autenticación debe retornar 401."""
    payload = {
        "nombre": "Nuevo Producto",
        "descripcion": "Descripción",
        "precio_base": 100.0
    }
    response = client.post("/api/v1/productos/", json=payload)
    assert response.status_code == 401


def test_create_producto_con_admin(admin_client):
    """POST / con admin debe crear producto (201)."""
    payload = {
        "nombre": "Nuevo Producto",
        "descripcion": "Una descripción",
        "precio_base": 150.0,
        "stock_cantidad": 20,
        "disponible": True
    }
    response = admin_client.post("/api/v1/productos/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["nombre"] == "Nuevo Producto"
    assert data["data"]["precio_base"] == 150.0
    assert data["data"]["stock_cantidad"] == 20


def test_create_producto_con_imagenes(admin_client):
    """POST con array de imágenes."""
    payload = {
        "nombre": "Producto con Fotos",
        "descripcion": "Tiene múltiples imágenes",
        "precio_base": 200.0,
        "imagenes_url": [
            "http://example.com/img1.jpg",
            "http://example.com/img2.jpg"
        ]
    }
    response = admin_client.post("/api/v1/productos/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert len(data["data"]["imagenes_url"]) == 2


def test_create_producto_stock_negativo(admin_client):
    """POST con stock negativo debe fallar validación Pydantic (422)."""
    payload = {
        "nombre": "Producto Inválido",
        "descripcion": "",
        "precio_base": 100.0,
        "stock_cantidad": -5  # Inválido
    }
    response = admin_client.post("/api/v1/productos/", json=payload)
    assert response.status_code == 422  # Validation error


def test_update_producto_sin_auth(client, session):
    """PUT sin autenticación debe retornar 401."""
    prod_data = ProductoCreate(nombre="Original", descripcion="", precio_base=100.0)
    prod = producto_service.create(session, prod_data)
    session.refresh(prod)

    payload = {"nombre": "Actualizado"}
    response = client.put(f"/api/v1/productos/{prod.id}", json=payload)
    assert response.status_code == 401


def test_update_producto_con_admin(admin_client, session):
    """PUT con admin debe actualizar producto."""
    prod_data = ProductoCreate(
        nombre="Original",
        descripcion="Desc original",
        precio_base=100.0,
        stock_cantidad=10
    )
    prod = producto_service.create(session, prod_data)
    session.refresh(prod)

    payload = {
        "nombre": "Actualizado",
        "precio_base": 150.0,
        "stock_cantidad": 20
    }
    response = admin_client.put(f"/api/v1/productos/{prod.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["nombre"] == "Actualizado"
    assert data["data"]["precio_base"] == 150.0
    assert data["data"]["stock_cantidad"] == 20


def test_update_producto_no_existente(admin_client):
    """PUT a producto inexistente."""
    payload = {"nombre": "No existe"}
    response = admin_client.put("/api/v1/productos/999", json=payload)
    data = response.json()
    assert data["success"] is False
    assert "no encontrado" in data["message"].lower()


def test_delete_producto_sin_auth(client, session):
    """DELETE sin autenticación debe retornar 401."""
    prod_data = ProductoCreate(nombre="Para borrar", descripcion="", precio_base=100.0)
    prod = producto_service.create(session, prod_data)
    session.refresh(prod)

    response = client.delete(f"/api/v1/productos/{prod.id}")
    assert response.status_code == 401


def test_delete_producto_con_admin(admin_client, session):
    """DELETE con admin debe soft-deletar producto."""
    prod_data = ProductoCreate(nombre="Para eliminar", descripcion="", precio_base=100.0)
    prod = producto_service.create(session, prod_data)
    session.refresh(prod)

    response = admin_client.delete(f"/api/v1/productos/{prod.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_delete_producto_no_existente(admin_client):
    """DELETE a producto inexistente."""
    response = admin_client.delete("/api/v1/productos/999")
    data = response.json()
    assert data["success"] is False
    assert "no encontrado" in data["message"].lower()


def test_patch_disponibilidad_sin_auth(client, session):
    """PATCH disponibilidad sin autenticación debe retornar 401."""
    prod_data = ProductoCreate(nombre="Producto", descripcion="", precio_base=100.0, disponible=True)
    prod = producto_service.create(session, prod_data)
    session.refresh(prod)

    response = client.patch(f"/api/v1/productos/{prod.id}/disponibilidad?disponible=false")
    assert response.status_code == 401


def test_patch_disponibilidad_con_admin(admin_client, session):
    """PATCH disponibilidad con admin debe cambiar el estado."""
    prod_data = ProductoCreate(nombre="Producto", descripcion="", precio_base=100.0, disponible=True)
    prod = producto_service.create(session, prod_data)
    session.refresh(prod)

    # Cambiar a no disponible
    response = admin_client.patch(f"/api/v1/productos/{prod.id}/disponibilidad?disponible=false")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["disponible"] is False

    # Cambiar a disponible nuevamente
    response = admin_client.patch(f"/api/v1/productos/{prod.id}/disponibilidad?disponible=true")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["disponible"] is True


def test_patch_disponibilidad_no_existente(admin_client):
    """PATCH disponibilidad a producto inexistente."""
    response = admin_client.patch("/api/v1/productos/999/disponibilidad?disponible=false")
    data = response.json()
    assert data["success"] is False
    assert "no encontrado" in data["message"].lower()
