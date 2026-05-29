from sqlmodel import Session
from app.catalogo.model import FormaPago, EstadoPedido, UnidadMedida
from app.core.constants import FORMAS_PAGO, ESTADOS_PEDIDO, UNIDADES_MEDIDA
from app.catalogo.unit_of_work import CatalogoUnitOfWork


def seed_catalogos(session: Session) -> None:
    """Inicializa los catálogos de FormaPago, EstadoPedido y UnidadMedida si no existen."""
    uow = CatalogoUnitOfWork(session)

    # Seed UnidadMedida
    for um_data in UNIDADES_MEDIDA:
        existing = uow.unidades_medida.get_by_id(um_data["codigo"])
        if not existing:
            new_um = UnidadMedida(**um_data)
            uow.unidades_medida.create(new_um)

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
