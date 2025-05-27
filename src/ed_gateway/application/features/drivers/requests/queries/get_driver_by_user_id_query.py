from dataclasses import dataclass

from ed_core.documentation.api.abc_core_api_client import DriverDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[DriverDto])
@dataclass
class GetDriverByUserIdQuery(Request):
    user_id: str
