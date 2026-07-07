# app/repositories/jobcard_repository.py

from typing import Generic
from typing import TypeVar

from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.maintenance import MaintenanceJobCard

class JobCardRepository(
    BaseRepository[MaintenanceJobCard]
):

    def __init__(self, db: Session):

        super().__init__(
            MaintenanceJobCard,
            db
        )

    def get_by_vehicle(
        self,
        vehicle_id: int
    ):

        return (
            self.db.query(
                MaintenanceJobCard
            )
            .filter(
                MaintenanceJobCard.vehicle_id
                == vehicle_id
            )
            .all()
        )