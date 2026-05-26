"""Tests para los routers de pedidos."""

import pytest
from app.venta.schema import PedidoCreate, DetallePedidoCreate, PagoCreate
from app.producto.schema import ProductoCreate
from app.venta import service as pedido_service
from app.producto import service as producto_service


def test_get_pedidos_sin_auth(client):
    """GET /api/v1/pedidos/ sin autenticación debe retornar 401."""
    response = client.get("/api/v1/pedidos/")
    assert response.status_code == 401


def test_get_pedidos_con_admin(admin_client, session, catalogo_seed):
    """GET /api/v1/pedidos/ con admin lista todos los pedidos."""
    # Crear 3 pedidos
    for i in range(3):
        pedido_data = PedidoCreate(
            usuario_id=1,
            estado_codigo="PENDIENTE",
            forma_pago_codigo="MERCADOPAGO",
            subtotal=100.0 * (i + 1),
            total=150.0 * (i + 1)
        )
        pedido_service.create_pedido(session, pedido_data)

    response = admin_client.get("/api/v1/pedidos/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total"] == 3
    assert len(data["data"]["items"]) == 3


def test_get_pedidos_paginacion(admin_client, session, catalogo_seed):
    """GET /api/v1/pedidos/ respeta limit y offset."""
    for i in range(5):
        pedido_data = PedidoCreate(
            usuario_id=1,
            estado_codigo="PENDIENTE",
            forma_pago_codigo="MERCADOPAGO",
            subtotal=100.0,
            total=150.0
        )
        pedido_service.create_pedido(session, pedido_data)

    # Primera página
    response = admin_client.get("/api/v1/pedidos/?limit=3&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["items"]) == 3
    assert data["data"]["total"] == 5

    # Segunda página
    response = admin_client.get("/api/v1/pedidos/?limit=3&offset=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["items"]) == 2


def test_get_pedido_por_id_con_admin(admin_client, session, catalogo_seed):
    """GET /api/v1/pedidos/{id} con admin."""
    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="PENDIENTE",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=100.0,
        total=150.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    response = admin_client.get(f"/api/v1/pedidos/{pedido.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == pedido.id
    assert data["data"]["usuario_id"] == 1


def test_get_pedido_no_existente(admin_client):
    """GET /api/v1/pedidos/{id} con pedido inexistente."""
    response = admin_client.get("/api/v1/pedidos/999")
    data = response.json()
    assert data["success"] is False


def test_create_pedido_sin_auth(client):
    """POST /api/v1/pedidos/ sin autenticación debe retornar 401."""
    payload = {
        "usuario_id": 1,
        "estado_codigo": "PENDIENTE",
        "forma_pago_codigo": "MERCADOPAGO",
        "subtotal": 100.0,
        "total": 150.0
    }
    response = client.post("/api/v1/pedidos/", json=payload)
    assert response.status_code == 401


def test_create_pedido_con_admin(admin_client, catalogo_seed):
    """POST /api/v1/pedidos/ con admin debe crear pedido (201)."""
    payload = {
        "usuario_id": 1,
        "estado_codigo": "PENDIENTE",
        "forma_pago_codigo": "MERCADOPAGO",
        "subtotal": 100.0,
        "total": 150.0,
        "notas": "Entregar rápido"
    }
    response = admin_client.post("/api/v1/pedidos/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["usuario_id"] == 1
    assert data["data"]["estado_codigo"] == "PENDIENTE"
    assert data["data"]["notas"] == "Entregar rápido"


def test_update_pedido_sin_auth(client, session, catalogo_seed):
    """PUT /api/v1/pedidos/{id} sin autenticación debe retornar 401."""
    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="PENDIENTE",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=100.0,
        total=150.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    payload = {"notas": "Nueva nota"}
    response = client.put(f"/api/v1/pedidos/{pedido.id}", json=payload)
    assert response.status_code == 401


def test_update_pedido_con_admin(admin_client, session, catalogo_seed):
    """PUT /api/v1/pedidos/{id} con admin debe actualizar."""
    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="PENDIENTE",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=100.0,
        total=150.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    payload = {
        "notas": "Entregar a la mañana",
        "costo_envio": 100.0
    }
    response = admin_client.put(f"/api/v1/pedidos/{pedido.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["notas"] == "Entregar a la mañana"
    assert data["data"]["costo_envio"] == 100.0


def test_delete_pedido_sin_auth(client, session, catalogo_seed):
    """DELETE /api/v1/pedidos/{id} sin autenticación debe retornar 401."""
    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="PENDIENTE",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=100.0,
        total=150.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    response = client.delete(f"/api/v1/pedidos/{pedido.id}")
    assert response.status_code == 401


def test_delete_pedido_con_admin(admin_client, session, catalogo_seed):
    """DELETE /api/v1/pedidos/{id} con admin debe soft-deletar."""
    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="PENDIENTE",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=100.0,
        total=150.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    response = admin_client.delete(f"/api/v1/pedidos/{pedido.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_transition_sin_auth(client, session, catalogo_seed):
    """POST /api/v1/pedidos/{id}/transition-estado sin auth debe retornar 401."""
    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="PENDIENTE",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=100.0,
        total=150.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    response = client.post(f"/api/v1/pedidos/{pedido.id}/transition-estado?accion=confirmar")
    assert response.status_code == 401


def test_transition_accion_confirmar(admin_client, session, catalogo_seed):
    """POST /api/v1/pedidos/{id}/transition-estado?accion=confirmar."""
    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="PENDIENTE",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=100.0,
        total=150.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    response = admin_client.post(f"/api/v1/pedidos/{pedido.id}/transition-estado?accion=confirmar")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["estado_codigo"] == "CONFIRMADO"


def test_transition_accion_preparar(admin_client, session, catalogo_seed):
    """POST /api/v1/pedidos/{id}/transition-estado?accion=preparar."""
    # Crear pedido en CONFIRMADO
    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="CONFIRMADO",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=100.0,
        total=150.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    response = admin_client.post(f"/api/v1/pedidos/{pedido.id}/transition-estado?accion=preparar")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["estado_codigo"] == "EN_PREP"


def test_transition_estado_invalido(admin_client, session, catalogo_seed):
    """POST transición prohibida debe fallar."""
    # Crear pedido en EN_CAMINO
    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="EN_CAMINO",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=100.0,
        total=150.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    # Intentar cancelar desde EN_CAMINO (no permitido)
    response = admin_client.post(
        f"/api/v1/pedidos/{pedido.id}/transition-estado?nuevo_estado=CANCELADO&motivo=test"
    )
    data = response.json()
    assert data["success"] is False


def test_transition_cancelar_sin_motivo(admin_client, session, catalogo_seed):
    """POST cancelar sin motivo debe fallar."""
    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="PENDIENTE",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=100.0,
        total=150.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    # Intentar cancelar sin motivo (obligatorio)
    response = admin_client.post(
        f"/api/v1/pedidos/{pedido.id}/transition-estado?nuevo_estado=CANCELADO"
    )
    data = response.json()
    assert data["success"] is False
    assert "motivo" in data["message"].lower()


def test_create_detalle_sin_auth(client, session, catalogo_seed):
    """POST /api/v1/pedidos/{id}/detalles sin auth debe retornar 401."""
    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="PENDIENTE",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=100.0,
        total=150.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    payload = {
        "producto_id": 1,
        "cantidad": 1,
        "nombre_snapshot": "Producto",
        "precio_snapshot": 100.0,
        "subtotal_snap": 100.0
    }
    response = client.post(f"/api/v1/pedidos/{pedido.id}/detalles", json=payload)
    assert response.status_code == 401


def test_create_detalle_con_admin(admin_client, session, catalogo_seed):
    """POST /api/v1/pedidos/{id}/detalles con admin."""
    # Crear producto
    prod_data = ProductoCreate(nombre="Hamburguesa", descripcion="", precio_base=500.0)
    producto = producto_service.create(session, prod_data)
    session.refresh(producto)

    # Crear pedido
    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="PENDIENTE",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=500.0,
        total=550.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    payload = {
        "pedido_id": pedido.id,
        "producto_id": producto.id,
        "cantidad": 2,
        "nombre_snapshot": "Hamburguesa",
        "precio_snapshot": 500.0,
        "subtotal_snap": 1000.0
    }
    response = admin_client.post(f"/api/v1/pedidos/{pedido.id}/detalles", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["cantidad"] == 2
    assert data["data"]["nombre_snapshot"] == "Hamburguesa"


def test_get_detalles_con_admin(admin_client, session, catalogo_seed):
    """GET /api/v1/pedidos/{id}/detalles con admin."""
    # Crear producto y pedido
    prod_data = ProductoCreate(nombre="Pizza", descripcion="", precio_base=800.0)
    producto = producto_service.create(session, prod_data)
    session.refresh(producto)

    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="PENDIENTE",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=800.0,
        total=850.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    # Crear detalle
    detalle_data = DetallePedidoCreate(
        pedido_id=pedido.id,
        producto_id=producto.id,
        cantidad=1,
        nombre_snapshot="Pizza",
        precio_snapshot=800.0,
        subtotal_snap=800.0
    )
    pedido_service.create_detalle_pedido(session, detalle_data)

    response = admin_client.get(f"/api/v1/pedidos/{pedido.id}/detalles")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) >= 1


def test_create_pago_con_admin(admin_client, session, catalogo_seed):
    """POST /api/v1/pedidos/{id}/pagos con admin."""
    # Crear pedido
    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="PENDIENTE",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=150.0,
        total=200.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    payload = {
        "pedido_id": pedido.id,
        "mp_status": "approved",
        "transaction_amount": 200.0,
        "external_reference": "REF123",
        "idempotency_key": "IDEM123"
    }
    response = admin_client.post(f"/api/v1/pedidos/{pedido.id}/pagos", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["mp_status"] == "approved"
    assert data["data"]["transaction_amount"] == 200.0


def test_update_pago_con_admin(admin_client, session, catalogo_seed):
    """PUT /api/v1/pedidos/{id}/pagos/{pago_id} con admin."""
    # Crear pedido
    pedido_data = PedidoCreate(
        usuario_id=1,
        estado_codigo="PENDIENTE",
        forma_pago_codigo="MERCADOPAGO",
        subtotal=150.0,
        total=200.0
    )
    pedido = pedido_service.create_pedido(session, pedido_data)
    session.refresh(pedido)

    # Crear pago
    pago_data = PagoCreate(
        pedido_id=pedido.id,
        mp_status="pending",
        transaction_amount=200.0,
        external_reference="REF456",
        idempotency_key="IDEM456"
    )
    pago = pedido_service.create_pago(session, pago_data)
    session.refresh(pago)

    # Actualizar pago
    payload = {
        "pedido_id": pedido.id,
        "mp_status": "approved",
        "mp_payment_id": 888888
    }
    response = admin_client.put(f"/api/v1/pedidos/{pedido.id}/pagos/{pago.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["mp_status"] == "approved"
    assert data["data"]["mp_payment_id"] == 888888
