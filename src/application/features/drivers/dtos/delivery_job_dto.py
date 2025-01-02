from datetime import datetime
from typing import TypedDict
from uuid import UUID

from src.domain.entities.order import Order
from src.domain.entities.route import Route


class DeliveryJobDto(TypedDict):
    id: UUID
    orders: list[Order]
    route: Route
    estimated_payment: float
    estimated_completion_time: datetime
