from sqlmodel import Session
from app.catalogo.model import FormaPago, EstadoPedido
from app.core.constants import FORMAS_PAGO, ESTADOS_PEDIDO
from app.catalogo.unit_of_work import CatalogoUnitOfWork


def seed_catalogos(session: Session) -> None:
    """Inicializa los catálogos de FormaPago y EstadoPedido si no existen."""
    uow = CatalogoUnitOfWork(session)

    # Seed FormaPago
    for fp_data in FORMAS_PAGO:
        existing = uow.formas_pago.get_by_id(fp_data["codigo"])
        if not existing:
            new_fp = FormaPago(**fp_data)
            uow.formas_pago.create(new_fp)

    # Seed EstadoPedido
    for ep_data in ESTADOS_PEDIDO:
        existing = uow.estados_pedido.get_by_id(ep_data["codigo"])
        if not existing:
            new_ep = EstadoPedido(**ep_data)
            uow.estados_pedido.create(new_ep)

    uow.commit()
