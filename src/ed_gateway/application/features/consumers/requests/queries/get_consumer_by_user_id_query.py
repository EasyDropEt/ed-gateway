from dataclasses import dataclass

from ed_core.documentation.abc_core_api_client import ConsumerDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[ConsumerDto])
@dataclass
class GetConsumerByUserIdQuery(Request):
    user_id: str
