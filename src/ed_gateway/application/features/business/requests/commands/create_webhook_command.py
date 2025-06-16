from dataclasses import dataclass
from uuid import UUID

from ed_core.documentation.api.abc_core_api_client import (CreateWebhookDto,
                                                           WebhookDto)
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[WebhookDto])
@dataclass
class CreateWebhookCommand(Request):
    business_id: UUID
    dto: CreateWebhookDto
