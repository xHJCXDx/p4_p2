from typing import Annotated, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
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
    limit: Annotated[int, Query(ge=1, le=100, description="Cantidad de productos por página")] = 10,
    offset: Annotated[int, Query(ge=0, description="Desplazamiento para paginación")] = 0,
    categoria_id: Annotated[Optional[int], Query(description="Filtrar por categoría")] = None,
    disponible: Annotated[Optional[bool], Query(description="Filtrar por disponibilidad")] = None,
    busqueda: Annotated[Optional[str], Query(description="Buscar por nombre")] = None,
) -> ApiResponse:
    """Listado público de productos con filtros: categoría, disponibilidad, búsqueda."""
    statement = select(Producto).where(Producto.deleted_at.is_(None)).options(
        selectinload(Producto.categorias),
        selectinload(Producto.ingredientes),
    )

    if busqueda:
        statement = statement.where(Producto.nombre.ilike(f"%{busqueda}%"))

    if categoria_id is not None:
        from app.producto.model import ProductoCategoriaLink
        statement = statement.join(ProductoCategoriaLink).where(
            ProductoCategoriaLink.categoria_id == categoria_id
        )

    count_statement = select(Producto).where(Producto.deleted_at.is_(None))
    if busqueda:
        count_statement = count_statement.where(Producto.nombre.ilike(f"%{busqueda}%"))
    if categoria_id is not None:
        from app.producto.model import ProductoCategoriaLink
        count_statement = count_statement.join(ProductoCategoriaLink).where(
            ProductoCategoriaLink.categoria_id == categoria_id
        )
    total = len(session.exec(count_statement).all())

    statement = statement.offset(offset).limit(limit)
    productos = session.exec(statement).unique().all()

    # Construir respuesta con stock calculado
    items = [service.build_producto_read(session, p) for p in productos]

    # Filtrar por disponibilidad si se pidió (post-cálculo)
    if disponible is not None:
        items = [p for p in items if p.disponible == disponible]

    return success_response(
        data={
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset
        },
        message="Productos obtenidos exitosamente"
    )

@router.get("/{producto_id}")
def read_producto(producto_id: int, session: Session = Depends(get_session)) -> ApiResponse:
    """Detalle público de un producto por ID."""
    statement = (
        select(Producto)
        .where(Producto.id == producto_id, Producto.deleted_at.is_(None))
        .options(selectinload(Producto.categorias), selectinload(Producto.ingredientes))
    )
    producto = session.exec(statement).first()
    if not producto:
        return error_response(message="Producto no encontrado", status_code=404)
    return success_response(
        data=service.build_producto_read(session, producto),
        message="Producto obtenido exitosamente"
    )

@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("ADMIN"))])
def create_producto(producto: ProductoCreate, session: Session = Depends(get_session)) -> ApiResponse:
    """Crear producto (solo ADMIN)."""
    new_producto = service.create(session, producto)
    return success_response(
        data=service.build_producto_read(session, new_producto),
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
        data=service.build_producto_read(session, updated_producto),
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
