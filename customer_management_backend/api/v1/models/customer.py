from uuid import UUID

from pydantic import BaseModel, constr


class CustomerUpdate(BaseModel):
    id: UUID
    first_name: constr(max_length=100)
    second_name: constr(max_length=100)
    address: constr(max_length=200)
    phone_number: constr(max_length=20)
