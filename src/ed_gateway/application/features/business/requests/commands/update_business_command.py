from dataclasses import dataclass
from uuid import UUID

from ed_core.documentation.api.abc_core_api_client import \
    BusinessDto as CoreBusinessDto
from ed_core.documentation.api.abc_core_api_client import UpdateBusinessDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[CoreBusinessDto])
@dataclass
class UpdateBusinessCommand(Request):
    business_id: UUID
    dto: UpdateBusinessDto
