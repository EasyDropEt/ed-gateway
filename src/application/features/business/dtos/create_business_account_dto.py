from typing import TypedDict
from uuid import UUID

from ed_domain_model.entities.business import BillingDetail


class CreateLocationDto(TypedDict):
    address: str
    latitude: float
    longitude: float
    postal_code: str
    city: str


class CreateBusinessAccountDto(TypedDict):
    user_id: UUID
    business_name: str
    owner_first_name: str
    owner_last_name: str
    phone_number: str
    email: str
    location: CreateLocationDto
    billing_details: list[BillingDetail]
