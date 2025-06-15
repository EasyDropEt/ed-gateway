from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from ed_core.documentation.api.abc_core_api_client import BusinessReportDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[BusinessReportDto])
@dataclass
class GetBusinessReportQuery(Request):
    business_id: UUID

    report_start_date: Optional[datetime]
    report_end_date: Optional[datetime]
