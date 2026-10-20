
from datetime import date

from pydantic import BaseModel, ConfigDict


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    department: str
    designation: str
    date_of_joining: date

    model_config = ConfigDict(from_attributes=True)
