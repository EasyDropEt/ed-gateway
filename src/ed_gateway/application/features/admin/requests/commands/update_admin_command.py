from dataclasses import dataclass
from uuid import UUID

from ed_core.documentation.api.abc_core_api_client import \
    AdminDto as CoreAdminDto
from ed_core.documentation.api.abc_core_api_client import UpdateAdminDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[CoreAdminDto])
@dataclass
class UpdateAdminCommand(Request):
    admin_id: UUID
    dto: UpdateAdminDto
