from datetime import datetime
from enum import StrEnum
from typing import NotRequired, TypedDict
from uuid import UUID

from src.domain.entities.driver_payment import DriverPayment
from src.domain.entities.route import Route


class DeliveryJobStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class DeliveryJob(TypedDict):
    id: UUID
    order_ids: list[UUID]
    route: Route
    driver_id: NotRequired[UUID]
    driver_payment: NotRequired[DriverPayment]
    status: DeliveryJobStatus
    estimated_payment: float
    estimated_completion_time: datetime
