from app.models.maintenance import (
    JobCardPart,
)

from app.repositories.jobcard_detail_repository import (
    JobCardDetailRepository, JobCardDetailRepository
)

from app.schemas.jobcard_detail import (
    JobCardDetailCreate,JobCardDetailCreate
)

from app.services.exceptions import (
    NotFoundException,
)


class JobCardDetailService:

    def __init__(
        self,
        jobcard_detail_repo: JobCardDetailRepository,
    ):

        self.jobcard_detail_repo = (
            jobcard_detail_repo
        )

    def create_jobcard_detail(
        self,
        payload: JobCardDetailCreate,
        user_id: int| None = None,
    ):

        jobcard_detail = JobCardPart(
            job_card_id=payload.job_card_id,
            part_id=payload.part_id,
            quantity=payload.quantity,
            unit_price=payload.unit_price,
            total_price=(
                payload.quantity
                * payload.unit_price
            ),
            modified_by=user_id,
        )

        return (
            self.jobcard_detail_repo.create(
                jobcard_detail
            )
        )

    def get_jobcard_detail(
        self,
        jobcard_detail_id: int,
    ):

        jobcard_detail = (
            self.jobcard_detail_repo.get_by_id(
                jobcard_detail_id
            )
        )

        if not jobcard_detail:
            raise NotFoundException(
                f"JobCardDetail "
                f"{jobcard_detail_id} "
                f"not found"
            )

        return jobcard_detail

    def get_all_jobcard_details(
        self,
    ):

        return (
            self.jobcard_detail_repo.get_all()
        )

    def get_parts_by_part_id(
        self,
        part_id: int,
    ):

        return (
            self.jobcard_detail_repo.get_by_part(
                part_id
            )
        )

    def update_jobcard_detail(
        self,
        jobcard_detail_id: int,
        payload,
        user_id: int| None = None,
    ):

        jobcard_detail = (
            self.get_jobcard_detail(
                jobcard_detail_id
            )
        )

        update_data = (
            payload.model_dump(
                exclude_unset=True
            )
        )
        update_data["modified_by"] = user_id
        return (
            self.jobcard_detail_repo
            .update_jobcard_detail(
                jobcard_detail,
                update_data,
            )
        )

    def delete_jobcard_detail(
        self,
        jobcard_detail_id: int,
    ):

        jobcard_detail = (
            self.get_jobcard_detail(
                jobcard_detail_id
            )
        )

        self.jobcard_detail_repo.delete(
            jobcard_detail
        )
