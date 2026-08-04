from fastapi import APIRouter   #type: ignore
from fastapi import Depends     #type: ignore
from sqlalchemy.orm import Session
from app.db.dependencies import get_db

from app.repositories.jobcard_detail_repository import (
    JobCardDetailRepository,
)
from app.repositories.complaint_repository import ( ComplaintRepository )
from app.repositories.inspection_repository import (InspectionRepository )
from app.repositories.vehicle_repository import (VehicleRepository )
from app.schemas.jobcard_detail import (
    JobCardDetailCreate,
    JobCardDetailResponse,
    JobCardDetailUpdate
)

from app.services.jobcard_detail_service import (
    JobCardDetailService
)
from app.api.dependencies import get_current_user_id


router = APIRouter(
    prefix="/api/v1/jobcard-detail",
    tags=["Job Card Part"]
)

#POST   /
#Create JobCardDetail
@router.post(
    "",
    response_model=JobCardDetailResponse,
    status_code=201,
)
def create_JobCardDetail(
    payload: JobCardDetailCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):

    service = JobCardDetailService(
        JobCardDetailRepository(db),
    )

    return service.create_jobcard_detail(
        payload
    )
#Get All
@router.get(
    "",
    response_model=list[JobCardDetailResponse],
)
def get_all_JobCardDetails(
    db: Session = Depends(get_db),
):

    service = JobCardDetailService(
        JobCardDetailRepository(db)
    )

    return (
        service.get_all_jobcard_details()
    )

#GET    /{JobCardDetail_id}
#Get JobCardDetail
@router.get(
    "/{JobCardDetail_id}",
    response_model=JobCardDetailResponse,
)
def get_JobCardDetail(
    JobCardDetail_id: int,
    db: Session = Depends(get_db),
):

    service = JobCardDetailService(
        JobCardDetailRepository(db)
    )

    return service.get_jobcard_detail(
        JobCardDetail_id
    )

#PUT    /{JobCardDetail_id}
#Update JobCardDetail
@router.put(
    "/{JobCardDetail_id}",
    response_model=JobCardDetailResponse,
)
def update_JobCardDetail(
    JobCardDetail_id: int,
    payload: JobCardDetailUpdate,
    db: Session = Depends(get_db),
):

    service = JobCardDetailService(
        JobCardDetailRepository(db)
    )

    return service.update_jobcard_detail(
        JobCardDetail_id,
        payload,
    )

#DELETE /{JobCardDetail_id}
#Delete JobCardDetail
@router.delete(
    "/{JobCardDetail_id}"
)
def delete_JobCardDetail(
    JobCardDetail_id: int,
    db: Session = Depends(get_db),
):

    service = JobCardDetailService(
        JobCardDetailRepository(db)
    )

    service.delete_jobcard_detail(
        JobCardDetail_id
    )

    return {
        "success": True,
        "message":
        "Vehicle deleted successfully",
    }
