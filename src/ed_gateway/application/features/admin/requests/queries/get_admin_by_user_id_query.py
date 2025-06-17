from dataclasses import dataclass

from ed_core.documentation.api.abc_core_api_client import AdminDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[AdminDto])
@dataclass
class GetAdminByUserIdQuery(Request):
    user_id: str
