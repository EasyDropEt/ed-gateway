from dataclasses import dataclass
from uuid import UUID

from ed_core.documentation.api.abc_core_api_client import \
    ConsumerDto as CoreConsumerDto
from ed_core.documentation.api.abc_core_api_client import UpdateConsumerDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[CoreConsumerDto])
@dataclass
class UpdateConsumerCommand(Request):
    consumer_id: UUID
    dto: UpdateConsumerDto
