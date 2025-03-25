from typing import Annotated

from fastapi import Depends
from rmediator import Mediator

from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.handlers.commands import (
    CreateDriverAccountCommandHandler,
    LoginDriverCommandHandler,
)
from ed_gateway.application.features.drivers.handlers.commands.login_driver_verify_command_handler import (
    LoginDriverVerifyCommandHandler,
)
from ed_gateway.application.features.drivers.requests.commands import (
    CreateDriverAccountCommand,
    LoginDriverCommand,
)
from ed_gateway.application.features.drivers.requests.commands.login_driver_verify_command import (
    LoginDriverVerifyCommand,
)
from ed_gateway.common.generic_helpers import get_config
from ed_gateway.common.typing.config import Config
from ed_gateway.infrastructure.api.api import Api


def api(config: Annotated[Config, Depends(get_config)]) -> ABCApi:
    return Api(config["core_api"], config["auth_api"])


def mediator(api: Annotated[ABCApi, Depends(api)]) -> Mediator:
    mediator = Mediator()

    # Driver features
    mediator.register_handler(
        CreateDriverAccountCommand, CreateDriverAccountCommandHandler(api)
    )
    mediator.register_handler(
        LoginDriverCommand, LoginDriverCommandHandler(api))
    mediator.register_handler(
        LoginDriverVerifyCommand, LoginDriverVerifyCommandHandler(api)
    )

    return mediator
