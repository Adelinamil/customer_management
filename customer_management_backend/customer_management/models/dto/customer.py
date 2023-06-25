from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Customer:
    id: UUID
    first_name: str
    second_name: str
    address: str
    phone_number: str
    created: datetime | None = None

    @classmethod
    def from_dict(cls, dct: dict) -> Customer:
        return Customer(
            id=dct['id'],
            first_name=dct['first_name'],
            second_name=dct['second_name'],
            address=dct['address'],
            phone_number=dct['phone_number']
        )
