from typing import NotRequired, TypedDict

from ed_core.application.features.common.dtos.create_consumer_dto import \
    CreateLocationDto


class UpdateConsumerDto(TypedDict):
    location: NotRequired[CreateLocationDto]
