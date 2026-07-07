from pydantic import BaseModel
from pydantic import ConfigDict


class JobCardPartCreate(BaseModel):

    job_card_id: int

    part_id: int

    quantity: float

    unit_price: float


class JobCardPartResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    job_card_id: int

    part_id: int