from fastapi import (APIRouter,Depends,)    #type: ignore

from sqlalchemy.orm import Session

from app.db.dependencies import (
    get_db,
)

from app.repositories.stock_ledger_repository import (
    StockLedgerRepository,
)

from app.schemas.stock_ledger_schema import (
    StockLedgerCreate,
    StockLedgerUpdate,
)

from app.services.stock_ledger_service import (
    StockLedgerService,
)

from app.repositories.part_repository import (
    PartRepository,
)
router = APIRouter(
    prefix="/api/v1/stock-ledger",
    tags=["Stock Ledger"],
)


def get_service(
    db: Session =
    Depends(get_db),
):

    return (StockLedgerService(
        StockLedgerRepository(db),
        PartRepository(db),
    ))


@router.post("")
def create_stock_ledger(
    payload: StockLedgerCreate,
    service:
    StockLedgerService =
    Depends(get_service),
):
    return service.create(payload)


@router.get("")
def get_stock_ledger(
    service:
    StockLedgerService =
    Depends(get_service),
):
    return service.get_all()


@router.get("/{ledger_id}")
def get_stock_ledger_by_id(
    ledger_id: int,
    service:
    StockLedgerService =
    Depends(get_service),
):
    return service.get_by_id(
        ledger_id
    )


@router.put("/{ledger_id}")
def update_stock_ledger(
    ledger_id: int,
    payload:
    StockLedgerUpdate,
    service:
    StockLedgerService =
    Depends(get_service),
):
    return service.update(
        ledger_id,
        payload,
    )


@router.delete("/{ledger_id}")
def delete_stock_ledger(
    ledger_id: int,
    service:
    StockLedgerService =
    Depends(get_service),
):
    return service.delete(
        ledger_id
    )


@router.get(
    "/balance/{part_id}"
)
def get_balance(
    part_id: int,
    service:
    StockLedgerService =
    Depends(get_service),
):
    return service.get_balance(
        part_id
    )
#Current Inventory Summary
@router.get("/dashboard/summary")
def get_inventory_summary(
    service: StockLedgerService =
    Depends(get_service),
):
    return service.get_inventory_summary()

#low stock parts with details
@router.get(
    "/dashboard/low-stock"
)
def get_low_stock_parts(
    service:
    StockLedgerService =
    Depends(get_service),
):
    return (
        service
        .get_low_stock_parts()
    )
@router.get(
    "/dashboard/top-consumed"
)
def get_top_consumed_parts(
    service:
    StockLedgerService =
    Depends(get_service),
):
    return (
        service
        .get_top_consumed_parts()
    )
@router.get(
    "/dashboard/top-returned"
)
def get_top_returned_parts(
    service:
    StockLedgerService =
    Depends(get_service),
):
    return (
        service
        .get_top_returned_parts()
    )
@router.get(
    "/dashboard/trend"
)
def get_issue_return_trend(
    service:
    StockLedgerService =
    Depends(get_service),
):
    return (
        service
        .get_issue_return_trend()
    )

