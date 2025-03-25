from dataclasses import dataclass

from ed_domain_model.services.auth.dtos import LoginUserVerifyDto
from ed_domain_model.services.core.dtos.driver_dto import DriverDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[DriverDto])
@dataclass
class LoginDriverVerifyCommand(Request):
    dto: LoginUserVerifyDto
