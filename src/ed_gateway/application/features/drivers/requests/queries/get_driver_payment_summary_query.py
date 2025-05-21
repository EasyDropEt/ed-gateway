from dataclasses import dataclass
from uuid import UUID

from ed_core.documentation.abc_core_api_client import DriverPaymentSummaryDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[DriverPaymentSummaryDto])
@dataclass
class GetDriverPaymentSummaryQuery(Request):
    driver_id: UUID
