from dataclasses import dataclass

from ed_domain_model.services.auth.dtos import UnverifiedUserDto
from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.drivers.dtos.login_driver_dto import LoginDriverDto


@request(BaseResponse[UnverifiedUserDto])
@dataclass
class LoginDriverCommand(Request):
    dto: LoginDriverDto
