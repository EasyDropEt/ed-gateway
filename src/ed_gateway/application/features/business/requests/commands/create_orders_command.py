from dataclasses import dataclass
from uuid import UUID

from ed_core.documentation.api.abc_core_api_client import CreateOrdersDto, OrderDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[list[OrderDto]])
@dataclass
class CreateOrdersCommand(Request):
    business_id: UUID
    dto: CreateOrdersDto
