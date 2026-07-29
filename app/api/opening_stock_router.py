from fastapi import (APIRouter,Depends,)    #type: ignore

from sqlalchemy.orm import (
    Session,
)

from app.db.dependencies import (
    get_db,
)

from app.repositories.opening_stock_repository import (
    OpeningStockRepository,
)

from app.repositories.stock_ledger_repository import (
    StockLedgerRepository,
)

from app.schemas.opening_stock_schema import (
    OpeningStockCreate,
    OpeningStockUpdate,
    OpeningStockResponse
)

from app.services.opening_stock_service import (
    OpeningStockService,
)

router = APIRouter(
    prefix="/api/v1/opening-stock",
    tags=["Opening Stock"],
)


def get_service(
    db: Session =
    Depends(get_db),
):

    return (
        OpeningStockService(
            repository=OpeningStockRepository(db),
            stock_ledger_repository=StockLedgerRepository(db),
        )
    )


@router.post("",
             response_model=OpeningStockResponse)
def create_opening_stock(
    payload: OpeningStockCreate,
    service:
    OpeningStockService =
    Depends(get_service),
):
    return service.create(payload)


@router.get("")

def get_opening_stock(
    service:
    OpeningStockService =
    Depends(get_service),
):
    return service.get_all()


@router.get(
    "/{opening_stock_id}",
             response_model=OpeningStockResponse)

def get_opening_stock_by_id(
    opening_stock_id: int,
    service:
    OpeningStockService =
    Depends(get_service),
):
    return service.get_by_id(
        opening_stock_id
    )


@router.put(
    "/{opening_stock_id}",
             response_model=OpeningStockResponse)

def update_opening_stock(
    opening_stock_id: int,
    payload:
    OpeningStockUpdate,
    service:
    OpeningStockService =
    Depends(get_service),
):
    return service.update(
        opening_stock_id,
        payload,
    )


@router.delete(
    "/{opening_stock_id}"
)
def delete_opening_stock(
    opening_stock_id: int,
    service:
    OpeningStockService =
    Depends(get_service),
):
    return service.delete(
        opening_stock_id
    )