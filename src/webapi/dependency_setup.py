from typing import Annotated

from fastapi import Depends
from rmediator import Mediator

from src.application.contracts.infrastructure.api.abc_api import ABCApi
from src.application.features.drivers.handlers.commands import (
    CreateDriverAccountCommandHandler, LoginDriverCommandHandler)
from src.application.features.drivers.handlers.commands.login_driver_verify_command_handler import \
    LoginDriverVerifyCommandHandler
from src.application.features.drivers.requests.commands import (
    CreateDriverAccountCommand, LoginDriverCommand)
from src.application.features.drivers.requests.commands.login_driver_verify_command import \
    LoginDriverVerifyCommand
from src.common.generic_helpers import get_config
from src.common.typing.config import Config
from src.infrastructure.api.api import Api


def api(config: Annotated[Config, Depends(get_config)]) -> ABCApi:
    return Api(config['core_api'], config['auth_api'])

def mediator(api: Annotated[ABCApi, Depends(api)]) -> Mediator:
    mediator = Mediator()

    # Driver features
    mediator.register_handler(
        CreateDriverAccountCommand, CreateDriverAccountCommandHandler(api)
    )
    mediator.register_handler(LoginDriverCommand, LoginDriverCommandHandler(api))
    mediator.register_handler(LoginDriverVerifyCommand, LoginDriverVerifyCommandHandler(api))
    

    return mediator
