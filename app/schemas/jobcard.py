from datetime import date

from pydantic import BaseModel
from pydantic import ConfigDict


class JobCardCreate(BaseModel):

    complaint_id: int

    inspection_id: int

    vehicle_id: int

    maintenance_type_id: int | None = None

    severity_id: int | None = None

    labour_charges: float | None = None

    description: str | None = None


class JobCardUpdate(BaseModel):

    severity_id: int | None = None

    labour_charges: float | None = None

    job_status: str | None = None

    job_card_status: str | None = None

    description: str | None = None

    downtime_hours: float | None = None

    completion_date: date | None = None


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