from app.models.maintenance import MaintenanceJobCard
from app.schemas.jobcard import JobCardCreate,JobCardUpdate,JobCardResponse
from app.services.exceptions import NotFoundException

class JobCardService:

    def __init__(
        self,
        jobcard_repo,
        complaint_repo,
        vehicle_repo,
    ):

        self.jobcard_repo = (
            jobcard_repo
        )

        self.complaint_repo = (
            complaint_repo
        )

        self.jobcard_repo = (
            jobcard_repo
        )

        self.vehicle_repo = (
            vehicle_repo
        )
    def create_jobcard(
        self,
        payload
    ) -> JobCardCreate:

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
        jobcard_id: int,
    ) :

        jobcard = (
            self.jobcard_repo.get_by_id(
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

        return (
            self.jobcard_repo.get_all()
        )

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

    def update_jobcard(
        self,
        jobcard_id: int,
        payload: JobCardUpdate,
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

        return (
            self.jobcard_repo
            .update_job(
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