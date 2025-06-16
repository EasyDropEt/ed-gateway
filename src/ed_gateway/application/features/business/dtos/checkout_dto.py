from pydantic import BaseModel


class CheckoutDto(BaseModel):
    url: str
