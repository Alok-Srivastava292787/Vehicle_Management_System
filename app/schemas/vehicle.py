from datetime import date

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class VehicleCreate(BaseModel):

    vehicle_type_id: int | None = None

    fuel_type_id: int | None = None

    rc_number: str = Field(
        min_length=5,
        max_length=50
    )

    engine_no: str | None = None

    chassis_no: str | None = None

    purchase_date: date | None = None

    fuel_capacity: float | None = None


class VehicleUpdate(BaseModel):

    vehicle_type_id: int | None = None

    fuel_type_id: int | None = None

    rc_number: str | None = None

    engine_no: str | None = None

    chassis_no: str | None = None

    purchase_date: date | None = None

    fuel_capacity: float | None = None

    active_flag: bool | None = None


class VehicleResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    vehicle_id: int

    vehicle_type_id: int | None

    fuel_type_id: int | None

    rc_number: str

    engine_no: str | None

    chassis_no: str | None

    active_flag: bool