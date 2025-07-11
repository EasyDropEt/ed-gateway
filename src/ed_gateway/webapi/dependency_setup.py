from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from rmediator import Mediator

from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.contracts.infrastructure.email.abc_email_templater import \
    ABCEmailTemplater
from ed_gateway.application.contracts.infrastructure.image_upload.abc_image_uploader import \
    ABCImageUploader
from ed_gateway.application.features.admin.handlers.commands import (
    CreateAdminCommandHandler, LoginAdminCommandHandler,
    LoginAdminVerifyCommandHandler, SettleDriverPaymentCommandHandler,
    UpdateAdminCommandHandler)
from ed_gateway.application.features.admin.handlers.queries import (
    GetAdminByUserIdQueryHandler, GetAdminQueryHandler, GetAdminsQueryHandler)
from ed_gateway.application.features.admin.requests.commands import (
    CreateAdminCommand, LoginAdminCommand, LoginAdminVerifyCommand,
    SettleDriverPaymentCommand, UpdateAdminCommand)
from ed_gateway.application.features.admin.requests.queries import (
    GetAdminByUserIdQuery, GetAdminQuery, GetAdminsQuery)
from ed_gateway.application.features.business.handlers.commands import (
    CancelBusinessOrderCommandHandler, CheckoutCommandHandler,
    CreateApiKeyCommandHandler, CreateBusinessAccountCommandHandler,
    CreateOrderCommandHandler, CreateWebhookCommandHandler,
    DeleteApiKeyCommandHandler, InitializeCheckoutCommandHandler,
    LoginBusinessCommandHandler, LoginBusinessVerifyCommandHandler,
    UpdateBusinessCommandHandler)
from ed_gateway.application.features.business.handlers.queries import (
    GetBusinessApiKeysQueryHandler, GetBusinessByUserIdQueryHandler,
    GetBusinessesQueryHandler, GetBusinessOrdersQueryHandler,
    GetBusinessQueryHandler, GetBusinessReportQueryHandler,
    GetBusinessWebhookQueryHandler)
from ed_gateway.application.features.business.requests.commands import (
    CancelBusinessOrderCommand, CheckoutCommand, CreateApiKeyCommand,
    CreateBusinessAccountCommand, CreateOrderCommand, CreateWebhookCommand,
    DeleteApiKeyCommand, InitializeCheckoutCommand, LoginBusinessCommand,
    LoginBusinessVerifyCommand, UpdateBusinessCommand)
from ed_gateway.application.features.business.requests.queries import (
    GetBusinessApiKeysQuery, GetBusinessByUserIdQuery, GetBusinessesQuery,
    GetBusinessOrdersQuery, GetBusinessQuery, GetBusinessReportQuery,
    GetBusinessWebhookQuery)
from ed_gateway.application.features.consumers.handlers.commands import (
    CreateConsumerCommandHandler, LoginConsumerCommandHandler,
    LoginConsumerVerifyCommandHandler, RateDeliveryCommandHandler,
    UpdateConsumerCommandHandler)
from ed_gateway.application.features.consumers.handlers.queries import (
    GetConsumerByUserIdQueryHandler, GetConsumerOrdersQueryHandler,
    GetConsumerQueryHandler, GetConsumersQueryHandler)
from ed_gateway.application.features.consumers.requests.commands import (
    CreateConsumerCommand, LoginConsumerCommand, LoginConsumerVerifyCommand,
    RateDeliveryCommand, UpdateConsumerCommand)
from ed_gateway.application.features.consumers.requests.queries import (
    GetConsumerByUserIdQuery, GetConsumerOrdersQuery, GetConsumerQuery,
    GetConsumersQuery)
from ed_gateway.application.features.delivery_jobs.handlers.queries import (
    GetDeliveryJobQueryHandler, GetDeliveryJobsQueryHandler)
from ed_gateway.application.features.delivery_jobs.requests.queries import (
    GetDeliveryJobQuery, GetDeliveryJobsQuery)
from ed_gateway.application.features.drivers.handlers.commands import (
    ClaimDeliveryJobCommandHandler, CreateDriverAccountCommandHandler,
    FinishOrderDeliveryCommandHandler, FinishOrderPickUpCommandHandler,
    LoginDriverCommandHandler, LoginDriverVerifyCommandHandler,
    StartOrderDeliveryCommandHandler, StartOrderPickUpCommandHandler,
    UpdateDriverCurrentLocationCommandHandler)
from ed_gateway.application.features.drivers.handlers.queries import (
    GetDriverByIdQueryHandler, GetDriverByUserIdQueryHandler,
    GetDriverDeliveryJobsQueryHandler, GetDriverOrdersQueryHandler,
    GetDriverPaymentSummaryQueryHandler, GetDriversQueryHandler)
from ed_gateway.application.features.drivers.requests.commands import (
    ClaimDeliveryJobCommand, CreateDriverAccountCommand,
    FinishOrderDeliveryCommand, FinishOrderPickUpCommand, LoginDriverCommand,
    LoginDriverVerifyCommand, StartOrderDeliveryCommand,
    StartOrderPickUpCommand, UpdateDriverCurrentLocationCommand)
from ed_gateway.application.features.drivers.requests.queries import (
    GetDriverByIdQuery, GetDriverByUserIdQuery, GetDriverDeliveryJobsQuery,
    GetDriverOrdersQuery, GetDriverPaymentSummaryQuery, GetDriversQuery)
from ed_gateway.application.features.notifications.handlers.commands import \
    ReadNotificationCommandHandler
from ed_gateway.application.features.notifications.handlers.queries import \
    GetNotificationsQueryHandler
from ed_gateway.application.features.notifications.requests.commands import \
    ReadNotificationCommand
from ed_gateway.application.features.notifications.requests.queries import \
    GetNotificationsQuery
from ed_gateway.application.features.order.handlers.queries import (
    GetOrderQueryHandler, GetOrdersQueryHandler, TrackOrderQueryHandler)
from ed_gateway.application.features.order.requests.queries import (
    GetOrderQuery, GetOrdersQuery, TrackOrderQuery)
from ed_gateway.common.generic_helpers import get_config
from ed_gateway.common.typing.config import Config
from ed_gateway.infrastructure.api.api import Api
from ed_gateway.infrastructure.email.email_templater import EmailTemplater
from ed_gateway.infrastructure.image_upload.image_uploader import ImageUploader


def get_image_uploader(
    config: Annotated[Config, Depends(get_config)],
) -> ABCImageUploader:
    return ImageUploader(config["cloudinary"])


def api(config: Annotated[Config, Depends(get_config)]) -> ABCApi:
    return Api(config)


def email_templater() -> ABCEmailTemplater:
    return EmailTemplater()


def oauth_scheme(
    config: Annotated[Config, Depends(get_config)],
) -> OAuth2PasswordBearer:
    return OAuth2PasswordBearer(
        tokenUrl=f"{config['auth_api']}/token/verify",
        auto_error=False,
    )


def mediator(
    config: Annotated[Config, Depends(get_config)],
    email_templater: Annotated[ABCEmailTemplater, Depends(email_templater)],
    image_uploader: Annotated[ABCImageUploader, Depends(get_image_uploader)],
    api: Annotated[ABCApi, Depends(api)],
) -> Mediator:
    mediator = Mediator()

    features = [
        # Driver features
        (
            CreateDriverAccountCommand,
            CreateDriverAccountCommandHandler(
                api, image_uploader, email_templater),
        ),
        (LoginDriverCommand, LoginDriverCommandHandler(api)),
        (LoginDriverVerifyCommand, LoginDriverVerifyCommandHandler(api)),
        (GetDriverDeliveryJobsQuery, GetDriverDeliveryJobsQueryHandler(api)),
        (GetDriverByIdQuery, GetDriverByIdQueryHandler(api)),
        (GetDriverByUserIdQuery, GetDriverByUserIdQueryHandler(api)),
        (GetDriversQuery, GetDriversQueryHandler(api)),
        (GetDriverOrdersQuery, GetDriverOrdersQueryHandler(api)),
        (GetDriverPaymentSummaryQuery, GetDriverPaymentSummaryQueryHandler(api)),
        (ClaimDeliveryJobCommand, ClaimDeliveryJobCommandHandler(api)),
        (
            UpdateDriverCurrentLocationCommand,
            UpdateDriverCurrentLocationCommandHandler(api),
        ),
        (StartOrderPickUpCommand, StartOrderPickUpCommandHandler(api)),
        (FinishOrderPickUpCommand, FinishOrderPickUpCommandHandler(api)),
        (StartOrderDeliveryCommand, StartOrderDeliveryCommandHandler(api)),
        (FinishOrderDeliveryCommand, FinishOrderDeliveryCommandHandler(api)),
        # Business features
        (
            CreateBusinessAccountCommand,
            CreateBusinessAccountCommandHandler(api, email_templater),
        ),
        (LoginBusinessCommand, LoginBusinessCommandHandler(api)),
        (LoginBusinessVerifyCommand, LoginBusinessVerifyCommandHandler(api)),
        (GetBusinessQuery, GetBusinessQueryHandler(api)),
        (GetBusinessesQuery, GetBusinessesQueryHandler(api)),
        (GetBusinessOrdersQuery, GetBusinessOrdersQueryHandler(api)),
        (CreateOrderCommand, CreateOrderCommandHandler(api)),
        (GetBusinessByUserIdQuery, GetBusinessByUserIdQueryHandler(api)),
        (CancelBusinessOrderCommand, CancelBusinessOrderCommandHandler(api)),
        (UpdateBusinessCommand, UpdateBusinessCommandHandler(api)),
        (GetBusinessApiKeysQuery, GetBusinessApiKeysQueryHandler(api)),
        (CreateApiKeyCommand, CreateApiKeyCommandHandler(api)),
        (DeleteApiKeyCommand, DeleteApiKeyCommandHandler(api)),
        (GetBusinessReportQuery, GetBusinessReportQueryHandler(api)),
        (GetBusinessWebhookQuery, GetBusinessWebhookQueryHandler(api)),
        (CreateWebhookCommand, CreateWebhookCommandHandler(api)),
        (
            InitializeCheckoutCommand,
            InitializeCheckoutCommandHandler(api, config["checkout_base_url"]),
        ),
        (CheckoutCommand, CheckoutCommandHandler(api)),
        # Delivery features
        (GetDeliveryJobsQuery, GetDeliveryJobsQueryHandler(api)),
        (GetDeliveryJobQuery, GetDeliveryJobQueryHandler(api)),
        (GetDeliveryJobsQuery, GetDeliveryJobsQueryHandler(api)),
        # Consumer features
        (
            CreateConsumerCommand,
            CreateConsumerCommandHandler(api, image_uploader, email_templater),
        ),
        (LoginConsumerCommand, LoginConsumerCommandHandler(api)),
        (LoginConsumerVerifyCommand, LoginConsumerVerifyCommandHandler(api)),
        (GetConsumerByUserIdQuery, GetConsumerByUserIdQueryHandler(api)),
        (GetConsumerQuery, GetConsumerQueryHandler(api)),
        (GetConsumerOrdersQuery, GetConsumerOrdersQueryHandler(api)),
        (GetConsumersQuery, GetConsumersQueryHandler(api)),
        (RateDeliveryCommand, RateDeliveryCommandHandler(api)),
        (UpdateConsumerCommand, UpdateConsumerCommandHandler(api)),
        # Order features
        (TrackOrderQuery, TrackOrderQueryHandler(api)),
        (GetOrderQuery, GetOrderQueryHandler(api)),
        (GetOrdersQuery, GetOrdersQueryHandler(api)),
        # Notification features
        (GetNotificationsQuery, GetNotificationsQueryHandler(api)),
        (ReadNotificationCommand, ReadNotificationCommandHandler(api)),
        # Admin features
        (
            CreateAdminCommand,
            CreateAdminCommandHandler(api, image_uploader, email_templater),
        ),
        (LoginAdminCommand, LoginAdminCommandHandler(api)),
        (LoginAdminVerifyCommand, LoginAdminVerifyCommandHandler(api)),
        (GetAdminByUserIdQuery, GetAdminByUserIdQueryHandler(api)),
        (GetAdminQuery, GetAdminQueryHandler(api)),
        (GetAdminsQuery, GetAdminsQueryHandler(api)),
        (SettleDriverPaymentCommand, SettleDriverPaymentCommandHandler(api)),
        (UpdateAdminCommand, UpdateAdminCommandHandler(api)),
    ]

    for request, handler in features:
        mediator.register_handler(request, handler)

    return mediator
