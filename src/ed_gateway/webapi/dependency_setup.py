from typing import Annotated

from fastapi import Depends
from rmediator import Mediator

from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.handlers.commands import (
    CreateBusinessAccountCommandHandler, LoginBusinessCommandHandler,
    LoginBusinessVerifyCommandHandler)
from ed_gateway.application.features.business.requests.commands import (
    CreateBusinessAccountCommand, LoginBusinessCommand,
    LoginBusinessVerifyCommand)
from ed_gateway.application.features.delivery_jobs.handlers.queries import \
    GetDeliveryJobsQueryHandler
from ed_gateway.application.features.delivery_jobs.requests.queries import \
    GetDeliveryJobsQuery
from ed_gateway.application.features.drivers.handlers.commands import (
    CreateDriverAccountCommandHandler, LoginDriverCommandHandler,
    LoginDriverVerifyCommandHandler)
from ed_gateway.application.features.drivers.handlers.queries import (
    GetDriverByIdQueryHandler, GetDriverDeliveryJobsQueryHandler)
from ed_gateway.application.features.drivers.requests.commands import (
    CreateDriverAccountCommand, LoginDriverCommand, LoginDriverVerifyCommand)
from ed_gateway.application.features.drivers.requests.queries import (
    GetDriverByIdQuery, GetDriverDeliveryJobsQuery)
from ed_gateway.common.generic_helpers import get_config
from ed_gateway.common.typing.config import Config
from ed_gateway.infrastructure.api.api import Api


def api(config: Annotated[Config, Depends(get_config)]) -> ABCApi:
    return Api(config["core_api"], config["auth_api"])


def mediator(api: Annotated[ABCApi, Depends(api)]) -> Mediator:
    mediator = Mediator()

    features = [
        # Driver features
        (CreateDriverAccountCommand, CreateDriverAccountCommandHandler(api)),
        (LoginDriverCommand, LoginDriverCommandHandler(api)),
        (LoginDriverVerifyCommand, LoginDriverVerifyCommandHandler(api)),
        (GetDriverDeliveryJobsQuery, GetDriverDeliveryJobsQueryHandler(api)),
        (GetDriverByIdQuery, GetDriverByIdQueryHandler(api)),
        # Business features
        (CreateBusinessAccountCommand, CreateBusinessAccountCommandHandler(api)),
        (LoginBusinessCommand, LoginBusinessCommandHandler(api)),
        (LoginBusinessVerifyCommand, LoginBusinessVerifyCommandHandler(api)),
        # Delivery features
        (GetDeliveryJobsQuery, GetDeliveryJobsQueryHandler(api)),
    ]

    for request, handler in features:
        mediator.register_handler(request, handler)

    return mediator
