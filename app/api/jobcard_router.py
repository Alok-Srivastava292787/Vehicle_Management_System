from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db

from app.repositories.jobcard_repository import (
    JobCardRepository,
)
from app.repositories.inspection_repository import (
    InspectionRepository,
)

from app.repositories.complaint_repository import (
    ComplaintRepository,
)
from app.repositories.vehicle_repository import (
    VehicleRepository,
)
from app.repositories.jobcard_part_repository import JobCardPartRepository
from app.repositories.part_requisition_repository import PartRequisitionRepository
from app.repositories.part_requisition_detail_repository import PartRequisitionDetailRepository
from app.schemas.jobcard import (
    JobCardCreate,
    JobCardResponse,
    JobCardUpdate,
)

from app.services.jobcard_service import (
    JobCardService,
)
from app.api.dependencies import get_current_user_id


router = APIRouter(
    prefix="/api/v1/jobcards",
    tags=["Job Card"]
)

def get_service(
    db: Session =
    Depends(get_db),
):
    return JobCardService(
        jobcard_repo= JobCardRepository,
        complaint_repo= ComplaintRepository,
        vehicle_repo= VehicleRepository,
        inspection_repo= InspectionRepository,
        repository=JobCardRepository(db),
        job_card_part_repository=JobCardPartRepository(db),
        requisition_repository=PartRequisitionRepository(db),
        requisition_detail_repository=PartRequisitionDetailRepository(db),

        )

#POST   /
#Create JobCard
@router.post(
    "",
    response_model=JobCardResponse,
    status_code=201,
)
def create_JobCard(
    payload: JobCardCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):

    service = JobCardService(
        JobCardRepository(db),
        ComplaintRepository(db),
        VehicleRepository(db),
        InspectionRepository(db),
        JobCardRepository(db),
        JobCardPartRepository(db),
        PartRequisitionRepository(db),
        PartRequisitionDetailRepository(db),
    )

    return service.create_jobcard(
        payload
    )
#Get All
@router.get(
    "",
#    response_model=list[JobCardResponse],
)
def get_all_JobCards(
    db: Session = Depends(get_db),
):

    service = JobCardService(
        JobCardRepository(db),
        ComplaintRepository(db),
        VehicleRepository(db),
        InspectionRepository(db),
        JobCardRepository(db),
        JobCardPartRepository(db),
        PartRequisitionRepository(db),
        PartRequisitionDetailRepository(db),
    )
#    res=service.get_all_jobcard()
#    for item in res:
#        print(item.__dict__)
#return service.get_all_inspections()
    return (
        service.get_all_jobcard()
    )

#GET    /{JobCard_id}
#Get JobCard
@router.get(
    "/{JobCard_id}",
    response_model=JobCardResponse,
)
def get_JobCard(
    JobCard_id: int,
    db: Session = Depends(get_db),
):

    service = JobCardService(
        JobCardRepository(db),
        ComplaintRepository(db),
        VehicleRepository(db),
        InspectionRepository(db),
        JobCardRepository(db),
        JobCardPartRepository(db),
        PartRequisitionRepository(db),
        PartRequisitionDetailRepository(db),
    )

    return service.get_jobcard(
        JobCard_id
    )

#PUT    /{JobCard_id}
#Update JobCard
@router.put(
    "/{JobCard_id}",
    response_model=JobCardResponse,
)
def update_JobCard(
    JobCard_id: int,
    payload: JobCardUpdate,
    db: Session = Depends(get_db),
):

    service = JobCardService(
        JobCardRepository(db),
        ComplaintRepository(db),
        VehicleRepository(db),
        InspectionRepository(db),
        JobCardRepository(db),
        JobCardPartRepository(db),
        PartRequisitionRepository(db),
        PartRequisitionDetailRepository(db),
    )

    return service.update_jobcard(
        JobCard_id,
        payload,
    )

#DELETE /{JobCard_id}
#Delete JobCard
@router.delete(
    "/{JobCard_id}"
)
def delete_JobCard(
    JobCard_id: int,
    db: Session = Depends(get_db),
):

    service = JobCardService(
        JobCardRepository(db),
        ComplaintRepository(db),
        VehicleRepository(db),
        InspectionRepository(db),
        JobCardRepository(db),
        JobCardPartRepository(db),
        PartRequisitionRepository(db),
        PartRequisitionDetailRepository(db),
    )

    service.delete_jobcard(
        JobCard_id
    )

    return {
        "success": True,
        "message":
        "Vehicle deleted successfully",
    }
@router.post(
    "/{job_card_id}/generate-requisition"
)
def generate_requisition(
    job_card_id: int,
    service:
    JobCardService =
    Depends(get_service),
):

    return (
        service
        .generate_requisition(
            job_card_id
        )
    )