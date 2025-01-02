from datetime import datetime
from typing import TypedDict
from uuid import UUID

from src.domain.entities.consumer import Consumer
from src.domain.entities.order import Parcel


class CreateOrderDto(TypedDict):
    consumer: Consumer
    business_id: UUID
    latest_time_of_arrival: datetime
    parcel: Parcel
