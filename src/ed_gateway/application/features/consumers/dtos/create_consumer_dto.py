from typing import TypedDict

from ed_core.application.features.consumer.dtos.create_consumer_dto import \
    CreateLocationDto


class CreateConsumerDto(TypedDict):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    location: CreateLocationDto
