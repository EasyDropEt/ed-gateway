from dataclasses import dataclass
from uuid import UUID

from ed_core.documentation.abc_core_api_client import DriverHeldFundsDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[list[DriverHeldFundsDto]])
@dataclass
class GetDriverHeldFundsQuery(Request):
    driver_id: UUID
