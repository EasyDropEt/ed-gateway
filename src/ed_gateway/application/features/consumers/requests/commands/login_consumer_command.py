from dataclasses import dataclass

from ed_auth.application.features.auth.dtos import UnverifiedUserDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.features.consumers.dtos.login_consumer_dto import \
    LoginConsumerDto


@request(BaseResponse[UnverifiedUserDto])
@dataclass
class LoginConsumerCommand(Request):
    dto: LoginConsumerDto
