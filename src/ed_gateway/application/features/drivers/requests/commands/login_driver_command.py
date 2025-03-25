from dataclasses import dataclass

from ed_auth.application.features.auth.dtos import UnverifiedUserDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.features.drivers.dtos.login_driver_dto import \
    LoginDriverDto


@request(BaseResponse[UnverifiedUserDto])
@dataclass
class LoginDriverCommand(Request):
    dto: LoginDriverDto
