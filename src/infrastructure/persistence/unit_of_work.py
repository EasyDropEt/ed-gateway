from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.infrastructure.persistence.db_client import DbClient


class UnitOfWork(ABCUnitOfWork):
    def __init__(self, db_client: DbClient) -> None: ...
