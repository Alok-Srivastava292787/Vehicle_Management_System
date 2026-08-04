# app/repositories/jobcard_s=detail_repository.py


from sqlalchemy.orm import Session
from app.repositories.base_repository import (BaseRepository,)
from app.models.maintenance import (    JobCardPart)


class JobCardDetailRepository(
    BaseRepository[JobCardPart]
):

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(
            JobCardPart,
            db,
        )

    def get_by_id(
        self,
        job_card_id: int,
    ) -> JobCardPart | None:

        return (
            self.db.query(JobCardPart)
            .filter(
                JobCardPart.job_card_id
                == job_card_id
            )
            .first()
        )

    def get_by_jobcard(
        self,
        job_card_id: int,
    ) -> list:
        return (
            self.db.query(JobCardPart)
            .filter(
                JobCardPart.job_card_id
                == job_card_id
            )
            .all()
        )

    def get_by_part(
        self,
        part_id: int,
    ) -> list:
        return (
            self.db.query(JobCardPart)
            .filter(
                JobCardPart.part_id
                == part_id
            )
            .all()
        )
    
    def update_jobcard_detail(
        self,
        jobcard_detail: JobCardPart,
        data: dict,
    ) -> JobCardPart:

        for key, value in data.items():

            setattr(
                jobcard_detail,
                key,
                value,
            )

        self.db.commit()

        self.db.refresh(
            jobcard_detail
        )

        return jobcard_detail

    def delete_jobcard(
        self,
        jobcard: JobCardPart,
    ) -> None:

        self.db.delete(
            jobcard
        )

        self.db.commit()
    
    def exists(
    self,
    job_card_id: int
    ) -> bool:
    
        return (
            self.get_by_id(job_card_id)
            is not None
        )