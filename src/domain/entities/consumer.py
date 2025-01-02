from typing import TypedDict
from uuid import UUID


class Consumer(TypedDict):
    id: UUID
    name: str
    role: str
    phone_number: str
    email: str
    active_status: bool
    notification_ids: list[UUID]
