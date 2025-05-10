from dataclasses import dataclass
from uuid import UUID

from ed_core.documentation.abc_core_api_client import UpdateLocationDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[None])
@dataclass
class UpdateDriverCurrentLocationCommand(Request):
    driver_id: UUID
    dto: UpdateLocationDto
