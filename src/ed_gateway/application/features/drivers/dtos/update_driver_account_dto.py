from typing import NotRequired, TypedDict

from ed_core.application.features.driver.dtos.create_driver_dto import \
    CreateLocationDto


class UpdateDriverAccountDto(TypedDict):
    phone_number: NotRequired[str]
    email: NotRequired[str]
    location: NotRequired[CreateLocationDto]
    password: NotRequired[str]
