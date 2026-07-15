from __future__ import annotations
from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict

#InspectionCreate
class InspectionCreate(BaseModel):
    complaint_id: int
    technician_id: int
    observed_issue: str | None = None
    operator_notes: str | None = None
    status: str | None = None

#InspectionUpdate
class InspectionUpdate(BaseModel):
    observed_issue: str | None = None
    operator_notes: str | None = None
    status: str | None = None

#InspectionResponse
class InspectionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    inspection_id: int
    complaint_id: int
    technician_id: int
    observed_issue: str | None = None
    operator_notes: str | None = None
    status: str | None = None
    inspection_time: datetime | None = None
    created_by: int | None = None
    created_at: datetime | None = None
    modified_by: int | None = None
    modified_at: datetime | None = None