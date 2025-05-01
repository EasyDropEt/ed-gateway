from dataclasses import dataclass

from ed_auth.application.features.auth.dtos import LoginUserVerifyDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.features.business.dtos import BusinessAccountDto


@request(BaseResponse[BusinessAccountDto])
@dataclass
class LoginBusinessVerifyCommand(Request):
    dto: LoginUserVerifyDto
