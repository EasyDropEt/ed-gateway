from datetime import datetime
from typing import TypedDict

from ed_core.application.features.business.dtos.create_order_dto import \
    CreateParcelDto
from ed_core.application.features.common.dtos import CreateLocationDto


class CreateOrderDto(TypedDict):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    location: CreateLocationDto
    latest_time_of_delivery: datetime
    parcel: CreateParcelDto
