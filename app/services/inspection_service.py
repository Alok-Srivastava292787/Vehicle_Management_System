from app.models.maintenance import TechnicianInspection

from app.repositories.complaint_repository import (
    ComplaintRepository,
)

from app.repositories.inspection_repository import (
    InspectionRepository,
)

from app.schemas.inspection import (
    InspectionCreate,
    InspectionUpdate,
)

from app.services.exceptions import (
    NotFoundException,
)


class InspectionService:

    def __init__(
        self,
        inspection_repo: InspectionRepository,
        complaint_repo: ComplaintRepository,
    ):

        self.inspection_repo = inspection_repo
        self.complaint_repo = complaint_repo

    def create_inspection(
        self,
        payload: InspectionCreate,
    ) -> TechnicianInspection:

        complaint = self.complaint_repo.get_by_id(
            payload.complaint_id
        )

        if not complaint:
            raise NotFoundException(
                f"Complaint "
                f"{payload.complaint_id} "
                f"not found"
            )

        inspection = TechnicianInspection(
            complaint_id=payload.complaint_id,
            technician_id=payload.technician_id,
            observed_issue=payload.observed_issue,
            operator_notes=payload.operator_notes,
            status=payload.status,
        )

        return self.inspection_repo.create(
            inspection
        )

    def get_inspection(
        self,
        inspection_id: int,
    ) -> TechnicianInspection:

        inspection = (
            self.inspection_repo.get_by_id(
                inspection_id
            )
        )

        if not inspection:
            raise NotFoundException(
                f"Inspection "
                f"{inspection_id} "
                f"not found"
            )

        return inspection

    def get_all_inspections(
        self,
    ):

        return (
            self.inspection_repo.get_all()
        )

    def get_by_complaint(
        self,
        complaint_id: int,
    ):

        return (
            self.inspection_repo
            .get_by_complaint(
                complaint_id
            )
        )

    def update_inspection(
        self,
        inspection_id: int,
        payload: InspectionUpdate,
    ):

        inspection = (
            self.get_inspection(
                inspection_id
            )
        )

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )

        return (
            self.inspection_repo
            .update_inspection(
                inspection,
                update_data
            )
        )

    def delete_inspection(
        self,
        inspection_id: int,
    ) -> None:

        inspection = (
            self.get_inspection(
                inspection_id
            )
        )

        self.inspection_repo.delete(
            inspection
        )