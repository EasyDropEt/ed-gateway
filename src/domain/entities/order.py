from datetime import datetime
from enum import StrEnum
from typing import NotRequired, TypedDict
from uuid import UUID

from src.domain.entities.consumer import Consumer


class ParcelSize(StrEnum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class OrderStatus(StrEnum):
    PENDING = "PENDING"
    PICKED_UP = "PICKED_UP"
    DELIVERED = "DELIVERED"


class ParcelDimensions(TypedDict):
    length: int
    width: int
    height: float


class Parcel(TypedDict):
    size: ParcelSize
    weight: float
    dimensions: ParcelDimensions
    fragile: bool


class Order(TypedDict):
    id: UUID
    consumer: Consumer
    business_id: UUID
    bill_id: UUID
    latest_time_of_arrival: datetime
    parcel: Parcel
    status: OrderStatus
    delivery_time: NotRequired[datetime]
