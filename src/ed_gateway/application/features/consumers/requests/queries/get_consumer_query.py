from dataclasses import dataclass
from uuid import UUID

from ed_core.documentation.api.abc_core_api_client import ConsumerDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[ConsumerDto])
@dataclass
class GetConsumerQuery(Request):
    consumer_id: UUID
