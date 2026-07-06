from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class InspectionCreate(BaseModel):

    complaint_id: int

    technician_id: int

    observed_issue: str | None = None

    operator_notes: str | None = None

    status: str | None = None


class InspectionUpdate(BaseModel):

    observed_issue: str | None = None

    operator_notes: str | None = None

    status: str | None = None


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