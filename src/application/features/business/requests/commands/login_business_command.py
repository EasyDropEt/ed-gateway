from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.business.dtos import BusinessAccountDto, LoginBusinessDto


@request(BaseResponse[BusinessAccountDto])
@dataclass
class LoginBusinessCommand(Request):
    dto: LoginBusinessDto
