from dataclasses import dataclass

from ed_core.documentation.api.abc_core_api_client import \
    AdminDto as CoreAdminDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.features.admin.dtos import CreateAdminDto


@request(BaseResponse[CoreAdminDto])
@dataclass
class CreateAdminCommand(Request):
    dto: CreateAdminDto
