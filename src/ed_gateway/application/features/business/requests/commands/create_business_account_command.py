from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.features.business.dtos import (
    BusinessAccountDto, CreateBusinessAccountDto)


@request(BaseResponse[BusinessAccountDto])
@dataclass
class CreateBusinessAccountCommand(Request):
    dto: CreateBusinessAccountDto
