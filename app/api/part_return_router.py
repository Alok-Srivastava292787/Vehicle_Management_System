from fastapi import (APIRouter,Depends,)    #type: ignore

from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.repositories.part_return_repository import (
    PartReturnRepository,
)

from app.schemas.part_return_schema import (
    PartReturnCreate,
    PartReturnUpdate,
    PartReturnResponse,
)

from app.services.part_return_service import (
    PartReturnService,
)

router = APIRouter(
    prefix="/api/v1/part-returns",
    tags=["Part Returns"],
)


def get_service(
    db: Session = Depends(get_db),
):

    return PartReturnService(
        PartReturnRepository(db)
    )


@router.post("",
response_model=PartReturnResponse,
)
def create_part_return(
    payload: PartReturnCreate,
    service: PartReturnService = Depends(get_service),
):
    return service.create(payload)


@router.get("")
def get_part_returns(
    service: PartReturnService = Depends(get_service),
):
    return service.get_all()


@router.get("/{return_id}")
def get_part_return(
    return_id: int,
    service: PartReturnService = Depends(get_service),
):
    return service.get_by_id(return_id)


@router.put("/{return_id}")
def update_part_return(
    return_id: int,
    payload: PartReturnUpdate,
    service: PartReturnService = Depends(get_service),
):
    return service.update(
        return_id,
        payload,
    )


@router.delete("/{return_id}")
def delete_part_return(
    return_id: int,
    service: PartReturnService = Depends(get_service),
):
    return service.delete(
        return_id
    )