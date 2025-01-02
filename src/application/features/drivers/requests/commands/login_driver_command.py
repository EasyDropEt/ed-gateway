from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.drivers.dtos.driver_account_dto import DriverAccountDto
from src.application.features.drivers.dtos.login_driver_dto import LoginDriverDto


@request(BaseResponse[DriverAccountDto])
@dataclass
class LoginDriverCommand(Request):
    dto: LoginDriverDto
