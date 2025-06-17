from dataclasses import dataclass

from ed_auth.application.features.auth.dtos import LoginUserVerifyDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.features.admin.dtos import AdminDto


@request(BaseResponse[AdminDto])
@dataclass
class LoginAdminVerifyCommand(Request):
    dto: LoginUserVerifyDto
