from dataclasses import dataclass

from ed_core.documentation.api.abc_core_api_client import BusinessDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.features.business.dtos import \
    CreateBusinessAccountDto


@request(BaseResponse[BusinessDto])
@dataclass
class CreateBusinessAccountCommand(Request):
    dto: CreateBusinessAccountDto
