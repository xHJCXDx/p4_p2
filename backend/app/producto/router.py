from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.response import success_response, error_response, ApiResponse
from app.core.security import require_roles
from app.producto.schema import ProductoCreate, ProductoRead, ProductoUpdate
from app.producto.model import Producto
from app.producto import service

router = APIRouter(prefix="/api/v1/productos", tags=["Productos"])

@router.get("/")
def read_productos(
    session: Session = Depends(get_session),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    disponible: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    busqueda: Optional[str] = Query(None, description="Buscar por nombre")
) -> ApiResponse:
    """Listado público de productos con filtros: categoría, disponibilidad, búsqueda."""
    statement = select(Producto)

    # Filtro disponibilidad
    if disponible is not None:
        statement = statement.where(Producto.disponible == disponible)

    # Filtro búsqueda por nombre (case-insensitive)
    if busqueda:
        statement = statement.where(Producto.nombre.ilike(f"%{busqueda}%"))

    # Filtro categoría (requiere join)
    if categoria_id is not None:
        from app.producto.model import ProductoCategoriaLink
        statement = statement.join(ProductoCategoriaLink).where(
            ProductoCategoriaLink.categoria_id == categoria_id
        )

    # Contar total
    count_statement = select(Producto)
    if disponible is not None:
        count_statement = count_statement.where(Producto.disponible == disponible)
    if busqueda:
        count_statement = count_statement.where(Producto.nombre.ilike(f"%{busqueda}%"))
    if categoria_id is not None:
        from app.producto.model import ProductoCategoriaLink
        count_statement = count_statement.join(ProductoCategoriaLink).where(
            ProductoCategoriaLink.categoria_id == categoria_id
        )
    total = len(session.exec(count_statement).all())

    # Aplicar paginación
    statement = statement.offset(offset).limit(limit)
    productos = session.exec(statement).all()

    return success_response(
        data={
            "items": [ProductoRead.model_validate(p) for p in productos],
            "total": total,
            "limit": limit,
            "offset": offset
        },
        message="Productos obtenidos exitosamente"
    )

@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("ADMIN"))])
def create_producto(producto: ProductoCreate, session: Session = Depends(get_session)) -> ApiResponse:
    """Crear producto (solo ADMIN)."""
    new_producto = service.create(session, producto)
    return success_response(
        data=ProductoRead.model_validate(new_producto),
        message="Producto creado exitosamente",
        status_code=201
    )

@router.put("/{producto_id}", dependencies=[Depends(require_roles("ADMIN"))])
def update_producto(producto_id: int, producto: ProductoUpdate, session: Session = Depends(get_session)) -> ApiResponse:
    """Actualizar producto (solo ADMIN)."""
    db_producto = service.get_by_id(session, producto_id)
    if not db_producto:
        return error_response(message="Producto no encontrado", status_code=404)
    updated_producto = service.update(session, db_producto, producto)
    return success_response(
        data=ProductoRead.model_validate(updated_producto),
        message="Producto actualizado exitosamente"
    )

@router.delete("/{producto_id}", dependencies=[Depends(require_roles("ADMIN"))])
def delete_producto(producto_id: int, session: Session = Depends(get_session)) -> ApiResponse:
    """Eliminar producto (soft delete, solo ADMIN)."""
    db_producto = service.get_by_id(session, producto_id)
    if not db_producto:
        return error_response(message="Producto no encontrado", status_code=404)
    service.delete(session, db_producto)
    return success_response(
        message="Producto eliminado exitosamente",
        status_code=204
    )

@router.patch("/{producto_id}/disponibilidad", dependencies=[Depends(require_roles("ADMIN", "STOCK"))])
def toggle_disponibilidad(producto_id: int, disponible: bool = Query(...), session: Session = Depends(get_session)) -> ApiResponse:
    """Activar/desactivar disponibilidad de un producto (ADMIN o STOCK)."""
    db_producto = service.get_by_id(session, producto_id)
    if not db_producto:
        return error_response(message="Producto no encontrado", status_code=404)

    db_producto.disponible = disponible
    session.add(db_producto)
    session.commit()

    return success_response(
        data=ProductoRead.model_validate(db_producto),
        message=f"Producto {'activado' if disponible else 'desactivado'} exitosamente"
    )
