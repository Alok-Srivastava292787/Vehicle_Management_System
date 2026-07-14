from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class ComplaintCreate(BaseModel):
    vehicle_id: int
    driver_id: int 
    issue_description: str
    driver_reason: str | None = None


class ComplaintUpdate(BaseModel):
    issue_description: str | None = None
    driver_reason: str | None = None
    vehicle_received_at: datetime | None = None


class ComplaintResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    complaint_id: int
    vehicle_id: int
    driver_id: int
    issue_description: str | None = None
    driver_reason: str | None = None