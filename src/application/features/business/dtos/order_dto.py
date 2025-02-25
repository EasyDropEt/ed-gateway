from datetime import datetime
from typing import TypedDict
from uuid import UUID

from src.domain.entities.consumer import Consumer
from src.domain.entities.order import OrderStatus, Parcel


class OrderDto(TypedDict):
    id: UUID
    consumer: Consumer
    bill_id: UUID
    latest_time_of_arrival: datetime
    parcel: Parcel
    status: OrderStatus
    delivery_job_id: UUID
