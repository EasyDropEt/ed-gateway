from dataclasses import dataclass

from ed_core.documentation.abc_core_api_client import \
    ConsumerDto as CoreConsumerDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.features.consumers.dtos.create_consumer_dto import \
    CreateConsumerDto


@request(BaseResponse[CoreConsumerDto])
@dataclass
class CreateConsumerCommand(Request):
    dto: CreateConsumerDto
