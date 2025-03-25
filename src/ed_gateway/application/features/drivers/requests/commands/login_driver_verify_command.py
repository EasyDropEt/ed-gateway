from dataclasses import dataclass

from ed_auth.application.features.auth.dtos import LoginUserVerifyDto
from ed_domain.services.core.dtos.driver_dto import DriverDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[DriverDto])
@dataclass
class LoginDriverVerifyCommand(Request):
    dto: LoginUserVerifyDto
