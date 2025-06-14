from uuid import UUID

from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from ed_notification.documentation.api.abc_notification_api_client import \
    NotificationDto
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.notifications.requests.commands import \
    ReadNotificationCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(ReadNotificationCommand, BaseResponse[NotificationDto])
class ReadNotificationCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

        self._error_message = "Failed to fetch notifications."
        self._success_message = "Notifications fetched successfully."

    async def handle(
        self, request: ReadNotificationCommand
    ) -> BaseResponse[NotificationDto]:
        notification_dto = await self._update_notification(request.notification_id)

        return BaseResponse[NotificationDto].success(
            self._success_message, notification_dto
        )

    async def _update_notification(self, notification_id: UUID) -> NotificationDto:
        LOG.info(
            f"Calling notification update_notification API with notification_id: {notification_id}"
        )
        notification_response = await self._api.notification_api.update_notification(
            notification_id, {"read_status": True}
        )

        LOG.info(
            f"Received response from update_notification: {notification_response}")

        if not notification_response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[notification_response["http_status_code"]],
                self._error_message,
                notification_response["errors"],
            )

        return notification_response["data"]

    async def _get_notification(self, notification_id) -> NotificationDto:
        LOG.info(
            f"Calling notification get_notification_by_id API with notification_id: {notification_id}"
        )
        notification_response = await self._api.notification_api.get_notification_by_id(
            notification_id
        )

        LOG.info(
            f"Received response from get_notification_by_id {notification_response}"
        )

        if not notification_response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[notification_response["http_status_code"]],
                self._error_message,
                notification_response["errors"],
            )

        return notification_response["data"]
