from datetime import datetime
from enum import StrEnum
from typing import TypedDict
from uuid import UUID


class PaymentMethod(StrEnum):
    BANK_TRANSFER = "BANK_TRANSFER"
    TELEBIRR = "TELEBIRR"


class DriverPayment(TypedDict):
    amount: float
    status: str
    date: datetime
    payment_method: PaymentMethod


class Driver(TypedDict):
    id: UUID
    first_name: str
    last_name: str
    profile_picture: str
    license_number: str
    phone_number: str
    email: str
    location_id: UUID
    active_status: bool
    car_id: UUID
    assigned_delivery_job_ids: list[UUID]
    notification_ids: list[UUID]
    payment_history: list[DriverPayment]
