from typing import TypedDict


class LoginBusinessDto(TypedDict):
    phone_number: str
    password: str
