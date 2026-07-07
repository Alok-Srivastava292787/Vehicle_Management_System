# app/repositories/checklist_repository.py

from typing import Generic
from typing import TypeVar

from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.maintenance import MaintenanceJobCard

class ChecklistRepository(
    BaseRepository[
        PreventiveMaintenanceChecklist
    ]
):

    def __init__(self, db):

        super().__init__(
            PreventiveMaintenanceChecklist,
            db
        )