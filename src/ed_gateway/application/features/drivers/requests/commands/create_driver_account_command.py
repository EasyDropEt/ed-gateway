from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.features.drivers.dtos.create_driver_account_dto import (
    CreateDriverAccountDto,
)
from ed_gateway.application.features.drivers.dtos.driver_account_dto import (
    DriverAccountDto,
)


@request(BaseResponse[DriverAccountDto])
@dataclass
class CreateDriverAccountCommand(Request):
    dto: CreateDriverAccountDto
