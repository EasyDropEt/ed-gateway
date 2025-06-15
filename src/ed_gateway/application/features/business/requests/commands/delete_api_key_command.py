from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[None])
@dataclass
class DeleteApiKeyCommand(Request):
    business_id: UUID
    api_key_prefix: str
