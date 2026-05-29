from fastapi import APIRouter, Depends, status, Query
from pydantic import BaseModel
from sqlmodel import Session
from app.core.database import get_session
from app.core.response import success_response, error_response, ApiResponse
from app.core.security import require_roles
from app.ingrediente.schema import IngredienteCreate, IngredienteRead, IngredienteUpdate
from app.ingrediente import service
from app.catalogo.model import UnidadMedida
from app.catalogo.unit_of_work import CatalogoUnitOfWork

router = APIRouter(prefix="/api/v1/ingredientes", tags=["Ingredientes"])


class UnidadMedidaCreate(BaseModel):
    codigo: str
    nombre: str


@router.get("/unidades-medida")
def read_unidades_medida(session: Session = Depends(get_session)) -> ApiResponse:
    uow = CatalogoUnitOfWork(session)
    unidades = uow.unidades_medida.get_all_simple()
    return success_response(
        data=[{"codigo": u.codigo, "nombre": u.nombre} for u in unidades],
        message="Unidades de medida obtenidas"
    )


@router.post("/unidades-medida", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("ADMIN", "STOCK"))])
def create_unidad_medida(data: UnidadMedidaCreate, session: Session = Depends(get_session)) -> ApiResponse:
    uow = CatalogoUnitOfWork(session)
    existing = uow.unidades_medida.get_by_id(data.codigo)
    if existing:
        return error_response(message=f"La unidad '{data.codigo}' ya existe", status_code=400)
    new_um = UnidadMedida(codigo=data.codigo, nombre=data.nombre)
    uow.unidades_medida.create(new_um)
    uow.commit()
    return success_response(
        data={"codigo": new_um.codigo, "nombre": new_um.nombre},
        message="Unidad de medida creada",
        status_code=201
    )

@router.delete("/unidades-medida/{codigo}", dependencies=[Depends(require_roles("ADMIN", "STOCK"))])
def delete_unidad_medida(codigo: str, session: Session = Depends(get_session)) -> ApiResponse:
    uow = CatalogoUnitOfWork(session)
    um = uow.unidades_medida.get_by_id(codigo)
    if not um:
        return error_response(message="Unidad de medida no encontrada", status_code=404)
    from sqlmodel import select
    from app.ingrediente.model import Ingrediente
    en_uso = session.exec(
        select(Ingrediente).where(Ingrediente.unidad_medida_codigo == codigo)
    ).first()
    if en_uso:
        return error_response(
            message=f"No se puede eliminar: hay ingredientes usando '{codigo}'",
            status_code=400
        )
    session.delete(um)
    session.commit()
    return success_response(message="Unidad de medida eliminada")


@router.get("/")
def read_ingredientes(
    session: Session = Depends(get_session),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
) -> ApiResponse:
    ingredientes, total = service.get_all(session, limit, offset)

    return success_response(
        data={
            "items": [IngredienteRead.model_validate(i) for i in ingredientes],
            "total": total,
            "limit": limit,
            "offset": offset
        },
        message="Ingredientes obtenidos exitosamente"
    )

@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("ADMIN"))])
def create_ingrediente(ingrediente: IngredienteCreate, session: Session = Depends(get_session)) -> ApiResponse:
    """Crear ingrediente (solo ADMIN)."""
    new_ingrediente = service.create(session, ingrediente)
    return success_response(
        data=IngredienteRead.model_validate(new_ingrediente),
        message="Ingrediente creado exitosamente",
        status_code=201
    )

@router.put("/{ingrediente_id}", dependencies=[Depends(require_roles("ADMIN"))])
def update_ingrediente(ingrediente_id: int, ingrediente: IngredienteUpdate, session: Session = Depends(get_session)) -> ApiResponse:
    """Actualizar ingrediente (solo ADMIN)."""
    db_ingrediente = service.get_by_id(session, ingrediente_id)
    if not db_ingrediente:
        return error_response(message="Ingrediente no encontrado", status_code=404)
    updated_ingrediente = service.update(session, db_ingrediente, ingrediente)
    return success_response(
        data=IngredienteRead.model_validate(updated_ingrediente),
        message="Ingrediente actualizado exitosamente"
    )

@router.delete("/{ingrediente_id}", dependencies=[Depends(require_roles("ADMIN"))])
def delete_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)) -> ApiResponse:
    """Eliminar ingrediente (solo ADMIN)."""
    db_ingrediente = service.get_by_id(session, ingrediente_id)
    if not db_ingrediente:
        return error_response(message="Ingrediente no encontrado", status_code=404)
    service.delete(session, db_ingrediente)
    return success_response(
        message="Ingrediente eliminado exitosamente",
        status_code=204
    )
