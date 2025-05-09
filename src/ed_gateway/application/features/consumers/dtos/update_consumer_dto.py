from typing import NotRequired, TypedDict

from ed_core.application.features.consumer.dtos.create_consumer_dto import \
    CreateLocationDto


class UpdateConsumerDto(TypedDict):
    location: NotRequired[CreateLocationDto]
