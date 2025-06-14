from dataclasses import dataclass
from uuid import UUID

from ed_notification.documentation.api.abc_notification_api_client import \
    NotificationDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[NotificationDto])
@dataclass
class ReadNotificationCommand(Request):
    user_id: UUID
    notification_id: UUID
