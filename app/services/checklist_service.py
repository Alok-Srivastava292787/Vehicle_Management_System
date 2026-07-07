from app.models.maintenance import PreventiveMaintenanceChecklist

class ChecklistService:

    def __init__(
        self,
        checklist_repo
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