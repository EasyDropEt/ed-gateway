from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)


class UnitOfWork(ABCUnitOfWork):
    def __init__(self) -> None: ...
