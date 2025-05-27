from dataclasses import dataclass

from ed_core.documentation.api.abc_core_api_client import DriverDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.features.drivers.dtos.create_driver_account_dto import \
    CreateDriverAccountDto


@request(BaseResponse[DriverDto])
@dataclass
class CreateDriverAccountCommand(Request):
    dto: CreateDriverAccountDto
