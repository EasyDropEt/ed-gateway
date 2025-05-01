from typing import TypedDict

from ed_core.application.features.driver.dtos.create_driver_dto import (
    CreateCarDto, CreateLocationDto)


class CreateDriverAccountDto(TypedDict):
    first_name: str
    last_name: str
    profile_image: str
    phone_number: str
    email: str
    location: CreateLocationDto
    car: CreateCarDto
    password: str
