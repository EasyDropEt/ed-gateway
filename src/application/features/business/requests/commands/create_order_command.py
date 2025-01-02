from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.business.dtos.create_order_dto import CreateOrderDto
from src.application.features.business.dtos.order_dto import OrderDto


@request(BaseResponse[OrderDto])
@dataclass
class CreateOrderCommand(Request):
    dto: CreateOrderDto
