from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db

from app.repositories.jobcard_part_repository import (
    JobCardPartRepository,
)

from app.schemas.jobcard_part import (
    JobCardPartCreate,
    JobCardPartResponse,
)

from app.services.jobcard_service import (
    JobCardService,
)


router = APIRouter(
    prefix="/api/v1/jobcards",
    tags=["Job Card Part"]
)

#POST   /
#Create JobCardPart
@router.post(
    "",
    response_model=JobCardPartResponse,
    status_code=201,
)
def create_JobCardPart(
    payload: JobCardPartCreate,
    db: Session = Depends(get_db),
):

    service = JobCardService(
        JobCardPartRepository(db)
    )

    return service.create_JobCardPart(
        payload
    )
#Get All
@router.get(
    "",
    response_model=list[JobCardPartResponse],
)
def get_all_JobCardParts(
    db: Session = Depends(get_db),
):

    service = JobCardPartService(
        JobCardPartRepository(db)
    )

    return (
        service.get_all_JobCardParts()
    )

#GET    /{JobCardPart_id}
#Get JobCardPart
@router.get(
    "/{JobCardPart_id}",
    response_model=JobCardPartResponse,
)
def get_JobCardPart(
    JobCardPart_id: int,
    db: Session = Depends(get_db),
):

    service = JobCardPartService(
        JobCardPartRepository(db)
    )

    return service.get_JobCardPart(
        JobCardPart_id
    )

#PUT    /{JobCardPart_id}
#Update JobCardPart
@router.put(
    "/{JobCardPart_id}",
    response_model=JobCardPartResponse,
)
def update_JobCardPart(
    JobCardPart_id: int,
    payload: JobCardPartUpdate,
    db: Session = Depends(get_db),
):

    service = JobCardPartService(
        JobCardPartRepository(db)
    )

    return service.update_JobCardPart(
        JobCardPart_id,
        payload,
    )

#DELETE /{JobCardPart_id}
#Delete JobCardPart
@router.delete(
    "/{JobCardPart_id}"
)
def delete_JobCardPart(
    JobCardPart_id: int,
    db: Session = Depends(get_db),
):

    service = JobCardPartService(
        JobCardPartRepository(db)
    )

    service.delete_JobCardPart(
        JobCardPart_id
    )

    return {
        "success": True,
        "message":
        "Vehicle deleted successfully",
    }
