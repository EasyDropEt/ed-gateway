from rmediator.mediator import Mediator

from src.application.features.business.handlers.commands import (
    CreateBusinessAccountCommandHandler,
    CreateOrderCommandHandler,
    LoginBusinessCommandHandler,
)
from src.application.features.business.handlers.queries import (
    GetOrderByIdQueryHandler,
    GetOrdersQueryHandler,
)
from src.application.features.business.requests.commands import (
    CreateBusinessAccountCommand,
    CreateOrderCommand,
    LoginBusinessCommand,
)
from src.application.features.business.requests.queries import (
    GetOrderByIdQuery,
    GetOrdersQuery,
)
from src.application.features.drivers.handlers.commands import (
    CreateDriverAccountCommandHandler,
    LoginDriverCommandHandler,
)
from src.application.features.drivers.handlers.queries import (
    GetDeliveryJobByIdQueryHandler,
    GetDeliveryJobsQueryHandler,
)
from src.application.features.drivers.requests.commands import (
    CreateDriverAccountCommand,
    LoginDriverCommand,
)
from src.application.features.drivers.requests.queries import (
    GetDeliveryJobByIdQuery,
    GetDeliveryJobsQuery,
)
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.unit_of_work import UnitOfWork


def mediator() -> Mediator:
    # Dependencies
    db_client = DbClient()
    uow = UnitOfWork(db_client)

    # Driver features
    mediator = Mediator()

    mediator.register_handler(
        CreateDriverAccountCommand, CreateDriverAccountCommandHandler(uow)
    )
    mediator.register_handler(LoginDriverCommand, LoginDriverCommandHandler(uow))
    mediator.register_handler(
        GetDeliveryJobByIdQuery, GetDeliveryJobByIdQueryHandler(uow)
    )
    mediator.register_handler(GetDeliveryJobsQuery, GetDeliveryJobsQueryHandler(uow))

    # Business features
    mediator.register_handler(GetOrdersQuery, GetOrdersQueryHandler(uow))
    mediator.register_handler(GetOrderByIdQuery, GetOrderByIdQueryHandler(uow))
    mediator.register_handler(CreateOrderCommand, CreateOrderCommandHandler(uow))
    mediator.register_handler(LoginBusinessCommand, LoginBusinessCommandHandler(uow))
    mediator.register_handler(
        CreateBusinessAccountCommand, CreateBusinessAccountCommandHandler(uow)
    )
    mediator.register_handler(CreateOrderCommand, CreateOrderCommandHandler(uow))

    db_client.start()
    return mediator
