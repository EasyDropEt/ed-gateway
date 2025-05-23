from typing import TypedDict

from ed_core.application.features.business.dtos.create_location_dto import \
    CreateLocationDto
from ed_domain.core.entities.business import BillingDetail


class CreateBusinessAccountDto(TypedDict):
    business_name: str
    owner_first_name: str
    owner_last_name: str
    phone_number: str
    email: str
    location: CreateLocationDto
    billing_details: list[BillingDetail]
    password: str
