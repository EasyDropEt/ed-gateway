from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.drivers.dtos.create_driver_account_dto import \
    CreateDriverAccountDto
from src.application.features.drivers.dtos.driver_account_dto import \
    DriverAccountDto


@request(BaseResponse[DriverAccountDto])
@dataclass
class CreateDriverAccountCommand(Request):
    dto: CreateDriverAccountDto
