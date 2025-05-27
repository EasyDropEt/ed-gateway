from dataclasses import dataclass

from ed_core.documentation.api.abc_core_api_client import BusinessDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[BusinessDto])
@dataclass
class GetBusinessByUserIdQuery(Request):
    user_id: str
