from fastapi import (HTTPException,)    #type: ignore
from datetime import datetime

from app.models.part_requisition import (PartRequisition, PartRequisitionDetail)
from app.repositories.part_requisition_repository import (PartRequisitionRepository,)
from app.repositories.part_requisition_detail_repository import (PartRequisitionDetailRepository,)

from app.repositories.jobcard_part_repository import (JobCardPartRepository,)
from app.models.maintenance import MaintenanceJobCard
from app.schemas.jobcard import JobCardCreate,JobCardUpdate,JobCardResponse
from app.services.exceptions import NotFoundException
from app.repositories.jobcard_repository import (JobCardRepository,)
from app.repositories.complaint_repository import ComplaintRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.repositories.inspection_repository import InspectionRepository
from app.security.auth_dependency import get_current_user
class JobCardService:
    def __init__(
        self,
        jobcard_repo: JobCardRepository,
        complaint_repo: ComplaintRepository,
        vehicle_repo: VehicleRepository,
        inspection_repo: InspectionRepository,
        job_card_part_repository:       JobCardPartRepository,
        requisition_repository:         PartRequisitionRepository,
        requisition_detail_repository:  PartRequisitionDetailRepository,

    ):
        self.jobcard_repo = (          jobcard_repo)
        self.complaint_repo = (        complaint_repo)
        self.inspection_repo = (       inspection_repo)
        self.vehicle_repo = (          vehicle_repo)

        self.job_card_part_repository = (     job_card_part_repository)
        self.requisition_repository = (       requisition_repository)
        self.requisition_detail_repository = (requisition_detail_repository)

    def create_jobcard(
        self,
        payload,
        user_id: int| None = None,
    ) -> MaintenanceJobCard:

        if not self.vehicle_repo.exists(  payload.vehicle_id
        ):
            raise NotFoundException(        "Vehicle not found")

        if not self.complaint_repo.exists(
            payload.complaint_id
        ):
            raise NotFoundException(         "Complaint not found")

        if not self.inspection_repo.exists(
            payload.inspection_id
        ):
            raise NotFoundException(          "Inspection not found")
 
        jobcard = (
            MaintenanceJobCard(
                complaint_id=
                payload.complaint_id,
                inspection_id=
                payload.inspection_id,
                vehicle_id=
                payload.vehicle_id,
                labour_charges=
                payload.labour_charges,
                description=
                payload.description,
                modified_by=
                user_id,
                driver_id=payload.driver_id,
                technician1_id=payload.technician1_id,
                technician2_id=payload.technician2_id,
                date_time_in=payload.date_time_in,
                date_time_out=payload.date_time_out,
                zone_area=payload.zone_area,

                mileage_hours=payload.mileage_hours,
                maintenance_type=payload.maintenance_type,
                issue_reported=payload.issue_reported,
                problem_found_action_taken=payload.problem_found_action_taken,
                requisition_slip_number=payload.requisition_slip_number,
                requested_by_employee_id=payload.requested_by_employee_id,
                verified_by_employee_id=payload.verified_by_employee_id,
                approved_by_employee_id=payload.approved_by_employee_id,
                job_status=payload.job_status,
            )
        )

        if payload.driver_id is not None:
            jobcard.driver_id = payload.driver_id
        
        if payload.technician1_id is not None:
            jobcard.technician1_id = payload.technician1_id
        
        if payload.technician2_id is not None:
            jobcard.technician2_id = payload.technician2_id
        
        if payload.date_time_in is not None:
            jobcard.date_time_in = payload.date_time_in
        
        if payload.date_time_out is not None:
            jobcard.date_time_out = payload.date_time_out
        
        if payload.zone_area is not None:
            jobcard.zone_area = payload.zone_area
        
        if payload.mileage_hours is not None:
            jobcard.mileage_hours = payload.mileage_hours
        
        if payload.maintenance_type is not None:
            jobcard.maintenance_type = payload.maintenance_type
        
        if payload.issue_reported is not None:
            jobcard.issue_reported = payload.issue_reported
        
        if payload.problem_found_action_taken is not None:
            jobcard.problem_found_action_taken = (
                payload.problem_found_action_taken
            )
        
        if payload.requisition_slip_number is not None:
            jobcard.requisition_slip_number = (
                payload.requisition_slip_number
            )
        if payload.requested_by_employee_id is not None:
            jobcard.requested_by_employee_id = (
                payload.requested_by_employee_id
            )
        
        if payload.verified_by_employee_id is not None:
            jobcard.verified_by_employee_id = (
                payload.verified_by_employee_id
            )
        
        if payload.approved_by_employee_id is not None:
            jobcard.approved_by_employee_id = (
                payload.approved_by_employee_id
            )
        
        if payload.job_status is not None:
            jobcard.job_status = (
                payload.job_status
            )
        return (
            self.jobcard_repo
            .create(
                jobcard
            )
        )

    def get_jobcard(
        self,
        jobcard_id: int,
    ) :

        jobcard = (
            self.get_by_id(
                jobcard_id
            )
        )

        if not jobcard:
            raise NotFoundException(
                f"Inspection "
                f"{jobcard_id} "
                f"not found"
            )

        return jobcard

    def get_all_jobcard(
        self,
    ):

        job_cards = (
            self.jobcard_repo.get_all()
        )
        for job_card in job_cards:
            requisition = (
                self.requisition_repository
                .get_by_job_card_id(
                    job_card.job_card_id
                )
            )
            job_card.requisition_id = (
                requisition.requisition_id
                if requisition
                else None
            )
            setattr(
                job_card,
                "requisition_slip_number",
                requisition.requisition_number
                if requisition
                else None,
                )
        return job_cards

    def get_by_complaint(
        self,
        complaint_id: int,
    ):

        return (
            self.jobcard_repo
            .get_by_complaint(
                complaint_id
            )
        )

    def get_by_id(
        self,
        job_card_id: int,
    ):

        job_card = (
            self.jobcard_repo.get_by_id(
                job_card_id
            )
        )

        if not job_card:
            return None

        requisition = (
            self.requisition_repository
            .get_by_job_card_id(
                job_card_id
            )
        )

        job_card.requisition_id = (
            requisition.requisition_id
            if requisition
            else None
        )

        setattr(
            job_card,
            "requisition_slip_number",
            requisition.requisition_number
            if requisition
            else None,
            )
        return job_card

    def update_jobcard(
        self,
        jobcard_id: int,
        payload: JobCardUpdate,
        user_id: int| None = None,
    ):

        update = (
            self.get_jobcard(
                jobcard_id
            )
        )

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )
        update_data["modified_by"] = user_id
        
        return (
            self.jobcard_repo
            .update_jobcard(
                update,
                update_data
            )
        )

    def delete_jobcard(
        self,
        jobcard_id: int,
    ) -> None:

        jobcard = (
            self.get_jobcard(
                jobcard_id
            )
        )

        self.jobcard_repo.delete(
            jobcard
        )
    def generate_requisition_number(
    self,
):

        latest = (
            self.requisition_repository
            .get_all()
        )

        running_no = (
            len(latest) + 1
        )

        return (
            f"PR-2026-"
            f"{running_no:06d}"
        )
    def generate_requisition(
    self,
    job_card_id: int,
):

        job_card = (
            self.jobcard_repo
            .get_by_id(
                job_card_id
            )
        )

        if not job_card:

            raise HTTPException(
                status_code=404,
                detail=
                "Job Card not found",
            )

        existing = (
            self.requisition_repository
            .get_by_id(
                job_card_id
            )
        )

        if existing:

            raise HTTPException(
                status_code=400,
                detail=
                "Requisition already exists for Job Card",
            )

        job_card_parts = (
            self.job_card_part_repository
            .get_all()
        )

        job_card_parts = [
            item
            for item in job_card_parts
            if item.job_card_id
            == job_card_id
            and item.active_flag
        ]

        if not job_card_parts:

            raise HTTPException(
                status_code=400,
                detail=
                "No Job Card Parts found",
            )

        requisition = (
            PartRequisition(
                requisition_number=
                self.generate_requisition_number(),

                vehicle_id=
                job_card.vehicle_id,

                job_card_id=
                job_card.job_card_id,

                technician_id=job_card.technician1_id,

                status="OPEN",

                remarks=(
                    "Generated from "
                    f"Job Card "
                    f"{job_card.job_card_id}"
                ),
            )
        )

        requisition = (
            self.requisition_repository
            .create(
                requisition
            )
        )

        for item in job_card_parts:

            detail = (
                PartRequisitionDetail(
                    requisition_id=
                    requisition.requisition_id,

                    part_id=
                    item.part_id,

                    quantity_required=
                    item.quantity,

                    quantity_returned=0,

                    remarks=(
                        "Generated from "
                        "Job Card Part"
                    ),
                )
            )

            self.requisition_detail_repository.create(
                detail
            )

        return {
            "requisition_id":
            requisition.requisition_id,

            "requisition_number":
            requisition.requisition_number,
        }
#submit approval
    def submit_for_verification(
        self,
        job_card_id: int,
        current_user,
    ):
        job_card = (
            self.jobcard_repo
            .get_by_id(job_card_id)
        )
        
        if not job_card:

            raise HTTPException(
                status_code=404,
                detail="Job Card not found",
            )

        if job_card.job_status not in [
            "DRAFT",
            "OPEN",
        ]:

            raise HTTPException(
                status_code=400,
                detail="Job Card cannot be submitted",
            )

        job_card.job_status = "REQUESTED"
        job_card.requested_by_employee_id = (current_user.employee_id)
        job_card.requested_at = datetime.utcnow()

        return self.jobcard_repo.update(
            job_card
        )
#Verify
    def verify(
        self,
        job_card_id: int,
#        employee_id: int|None,
        current_user,
    ):

        job_card = (
            self.jobcard_repo
            .get_by_id(job_card_id)
        )

        if not job_card:

            raise HTTPException(
                status_code=404,
                detail="Job Card not found",
            )

        if (
            job_card.job_status
            != "REQUESTED"
        ):

            raise HTTPException(
                status_code=400,
                detail="Job Card must be REQUESTED first",
            )

        job_card.job_status = "VERIFIED"
        job_card.verified_by_employee_id = (current_user.employee_id)
        job_card.verified_at = datetime.utcnow()

        return self.jobcard_repo.update(
            job_card
        )
#Approval
    def approve(
        self,
        job_card_id: int,
#        employee_id: int|None,
        current_user,
    ):

        job_card = (
            self.jobcard_repo
            .get_by_id(job_card_id)
        )

        if not job_card:

            raise HTTPException(
                status_code=404,
                detail="Job Card not found",
            )

        if (
            job_card.job_status
            != "VERIFIED"
        ):

            raise HTTPException(
                status_code=400,
                detail="Job Card must be VERIFIED first",
            )

        job_card.job_status = "APPROVED"
        job_card.approved_by_employee_id = (current_user.employee_id)
        job_card.approved_at = datetime.utcnow()

        return self.jobcard_repo.update(
            job_card
        )
