from datetime import datetime
from enum import StrEnum
from typing import TypedDict


class PaymentMethod(StrEnum):
    BANK_TRANSFER = "BANK_TRANSFER"
    TELEBIRR = "TELEBIRR"


class DriverPayment(TypedDict):
    amount: float
    status: str
    date: datetime
    payment_method: PaymentMethod
