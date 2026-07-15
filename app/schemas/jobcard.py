from __future__ import annotations
from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict

#Create JobCard
class JobCardCreate(BaseModel):
    complaint_id: int
    inspection_id: int
    vehicle_id: int
    maintenance_type_id: int | None = None
    severity_id: int | None = None
    labour_charges: float | None = None
    description: str | None = None

#Update
class JobCardUpdate(BaseModel):
    severity_id: int | None = None
    labour_charges: float | None = None
    job_status: str | None = None
    job_card_status: str | None = None
    description: str | None = None
    downtime_hours: float | None = None
    completion_date: date | None = None

#Response
class JobCardResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    job_card_id: int
    complaint_id: int
    inspection_id: int
    vehicle_id: int
    maintenance_type_id: int | None = None
    severity_id: int | None = None
    labour_charges: float | None = None
    description: str | None = None
    completion_date: date | None = None

    created_by: int | None = None
    created_at: datetime | None = None
    modified_by: int | None = None
    modified_at: datetime | None = None