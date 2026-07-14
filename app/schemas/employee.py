from pydantic import BaseModel
from pydantic import ConfigDict


class EmployeeCreate(BaseModel):
    employee_type: str
    full_name: str
    phone_number: str


class EmployeeUpdate(BaseModel):
    employee_type: str | None = None
    full_name: str | None = None
    phone_number: str | None = None


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    employee_id: int
    employee_type: str
    full_name: str
    phone_number: str