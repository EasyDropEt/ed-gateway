from dataclasses import dataclass
from uuid import UUID

from ed_core.documentation.core_api_client import DriverDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[DriverDto])
@dataclass
class GetDriverByIdQuery(Request):
    driver_id: UUID
