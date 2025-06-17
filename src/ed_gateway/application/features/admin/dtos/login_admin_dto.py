from typing import TypedDict


class LoginAdminDto(TypedDict):
    phone_number: str
    password: str
