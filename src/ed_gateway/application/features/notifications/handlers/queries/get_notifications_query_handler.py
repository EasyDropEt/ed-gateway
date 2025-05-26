from ed_core.documentation.abc_core_api_client import NotificationDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.notifications.requests.queries import \
    GetNotificationsQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetNotificationsQuery, BaseResponse[list[NotificationDto]])
class GetNotificationsQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: GetNotificationsQuery
    ) -> BaseResponse[list[NotificationDto]]:
        LOG.info(
            f"Calling core get_user_notifications API with user_id: {request.user_id}"
        )
        response = self._api.core_api.get_user_notifications(
            str(request.user_id))

        LOG.info(f"Received response from get_user_notifications: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to fetch notifications.",
                response["errors"],
            )

        return BaseResponse[list[NotificationDto]].success(
            "Notifications fetched successfully.", response["data"]
        )
