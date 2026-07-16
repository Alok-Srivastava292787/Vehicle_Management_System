from __future__ import annotations
from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class JobCardPartCreate(BaseModel):
    job_card_id: int
    part_id: int
    quantity: float
    unit_price: float
    active_flag: bool | None = True



class JobCardPartResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int
    job_card_id: int
    part_id: int
    active_flag: bool | None = True


class JobCardPartUpdate(BaseModel):
    job_card_id: int
    part_id: int
    quantity: float
    unit_price: float
    active_flag: bool | None = True
