# app/repositories/jobcard_part_repository.py

from typing import Generic
from typing import TypeVar

from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.maintenance import JobCardPart

class JobCardPartRepository(
    BaseRepository[JobCardPart]
):

    def __init__(
        self,
        db: Session
    ):
        super().__init__(
            JobCardPart,
            db
        )