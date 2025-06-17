from typing import TypedDict

from ed_core.application.features.common.dtos import CreateLocationDto
from ed_domain.core.value_objects.roles import AdminRole


class CreateAdminDto(TypedDict):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    password: str
    location: CreateLocationDto
    role: AdminRole
