from app.models.maintenance import PreventiveMaintenanceChecklist

from app.repositories.checklist_repository import (
    ChecklistRepository,
)

from app.schemas.checklist import (
    PMChecklistCreate,
    PMChecklistResponse,
    PMChecklistUpdate
)

from app.services.exceptions import (
    DuplicateRecordException,
    NotFoundException,
)

from app.services.checklist_service import (
    PreventiveMaintenanceChecklist
)

class ChecklistService:

    def __init__(
        self,
        checklist_repo: ChecklistRepository
    ):

        self.checklist_repo = (
            checklist_repo
        )

    def create_checklist(
        self,
        payload
    ):

        checklist = (
            PreventiveMaintenanceChecklist(
                vehicle_id=
                payload.vehicle_id,

                technician_id=
                payload.technician_id,

                observation=
                payload.observation,

                issue_found=
                payload.issue_found,

                issue_description=
                payload.issue_description,
            )
        )

        return (
            self.checklist_repo
            .create(checklist)
        )
    def get_checklist(
        self,
        checklist_id: int
    ):

        checklist = (
            self.checklist_repo
            .get_by_id(checklist_id)
        )

        if not checklist:

            raise NotFoundException(
                f"PMChecklist "
                f"{checklist_id}"
                f" not found"
            )

        return checklist

    def get_all_checklists(self):

        return (
            self.checklist_repo.get_all()
        )

    def update_checklist(
        self,
        checklist_id: int,
        payload: PMChecklistUpdate
    ):

        checklist = (
            self.get_checklist(
                checklist_id
            )
        )

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )

        return (
            self.checklist_repo
            .update_checklist(
                checklist,
                update_data
            )
        )

    def delete_checklist(
        self,
        checklist_id: int
    ):

        checklist = (
            self.get_checklist(
                checklist_id
            )
        )

        self.checklist_repo.delete(
            checklist
        )