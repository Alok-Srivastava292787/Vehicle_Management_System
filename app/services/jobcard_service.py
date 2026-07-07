from app.models.maintenance import MaintenanceJobCard
class JobCardService:

    def __init__(
        self,
        jobcard_repo,
        complaint_repo,
        inspection_repo,
        vehicle_repo,
    ):

        self.jobcard_repo = (
            jobcard_repo
        )

        self.complaint_repo = (
            complaint_repo
        )

        self.inspection_repo = (
            inspection_repo
        )

        self.vehicle_repo = (
            vehicle_repo
        )
    def create_jobcard(
        self,
        payload
    ) -> jobcard_master:

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
            )
        )

        return (
            self.jobcard_repo
            .create(
                jobcard
            )
        )



    def get_jobcard(
        self,
        inspection_id: int,
    ) :

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