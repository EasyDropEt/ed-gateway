from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from rmediator import Mediator

from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.handlers.commands import (
    CreateBusinessAccountCommandHandler, CreateOrdersCommandHandler,
    LoginBusinessCommandHandler, LoginBusinessVerifyCommandHandler)
from ed_gateway.application.features.business.handlers.queries import (
    GetBusinessByUserIdQueryHandler, GetBusinessOrdersQueryHandler,
    GetBusinessQueryHandler)
from ed_gateway.application.features.business.requests.commands import (
    CreateBusinessAccountCommand, CreateOrdersCommand, LoginBusinessCommand,
    LoginBusinessVerifyCommand)
from ed_gateway.application.features.business.requests.queries import (
    GetBusinessByUserIdQuery, GetBusinessOrdersQuery, GetBusinessQuery)
from ed_gateway.application.features.delivery_jobs.handlers.queries import (
    GetDeliveryJobQueryHandler, GetDeliveryJobsQueryHandler)
from ed_gateway.application.features.delivery_jobs.requests.queries import (
    GetDeliveryJobQuery, GetDeliveryJobsQuery)
from ed_gateway.application.features.drivers.handlers.commands import (
    ClaimDeliveryJobCommandHandler, CreateDriverAccountCommandHandler,
    LoginDriverCommandHandler, LoginDriverVerifyCommandHandler)
from ed_gateway.application.features.drivers.handlers.queries import (
    GetDriverByIdQueryHandler, GetDriverByUserIdQueryHandler,
    GetDriverDeliveryJobsQueryHandler)
from ed_gateway.application.features.drivers.requests.commands import (
    ClaimDeliveryJobCommand, CreateDriverAccountCommand, LoginDriverCommand,
    LoginDriverVerifyCommand)
from ed_gateway.application.features.drivers.requests.queries import (
    GetDriverByIdQuery, GetDriverByUserIdQuery, GetDriverDeliveryJobsQuery)
from ed_gateway.common.generic_helpers import get_config
from ed_gateway.common.typing.config import Config
from ed_gateway.infrastructure.api.api import Api


def api(config: Annotated[Config, Depends(get_config)]) -> ABCApi:
    return Api(config["core_api"], config["auth_api"])


def oauth_scheme(
    config: Annotated[Config, Depends(get_config)],
) -> OAuth2PasswordBearer:
    return OAuth2PasswordBearer(
        tokenUrl=f"{config['auth_api']}/token/verify",
        auto_error=False,
    )


def mediator(api: Annotated[ABCApi, Depends(api)]) -> Mediator:
    mediator = Mediator()

    features = [
        # Driver features
        (CreateDriverAccountCommand, CreateDriverAccountCommandHandler(api)),
        (LoginDriverCommand, LoginDriverCommandHandler(api)),
        (LoginDriverVerifyCommand, LoginDriverVerifyCommandHandler(api)),
        (GetDriverDeliveryJobsQuery, GetDriverDeliveryJobsQueryHandler(api)),
        (GetDriverByIdQuery, GetDriverByIdQueryHandler(api)),
        (GetDriverByUserIdQuery, GetDriverByUserIdQueryHandler(api)),
        (ClaimDeliveryJobCommand, ClaimDeliveryJobCommandHandler(api)),
        # Business features
        (CreateBusinessAccountCommand, CreateBusinessAccountCommandHandler(api)),
        (LoginBusinessCommand, LoginBusinessCommandHandler(api)),
        (LoginBusinessVerifyCommand, LoginBusinessVerifyCommandHandler(api)),
        (GetBusinessOrdersQuery, GetBusinessOrdersQueryHandler(api)),
        (CreateOrdersCommand, CreateOrdersCommandHandler(api)),
        (GetBusinessQuery, GetBusinessQueryHandler(api)),
        (GetBusinessByUserIdQuery, GetBusinessByUserIdQueryHandler(api)),
        # Delivery features
        (GetDeliveryJobsQuery, GetDeliveryJobsQueryHandler(api)),
        (GetDeliveryJobQuery, GetDeliveryJobQueryHandler(api)),
    ]

    for request, handler in features:
        mediator.register_handler(request, handler)

    return mediator
