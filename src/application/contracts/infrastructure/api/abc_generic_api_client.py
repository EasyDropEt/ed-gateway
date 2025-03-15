from abc import ABCMeta, abstractmethod
from typing import Generic, List, TypedDict, TypeVar
from uuid import UUID

CreateDto = TypeVar("CreateDto")
UpdateDto = TypeVar("UpdateDto")
Entity = TypeVar("Entity")


class GenericResponse(Generic[Entity], TypedDict): 
  success: bool
  message: str
  data: Entity
  errors: list[str]


class ABCGenericApiClient(Generic[CreateDto, UpdateDto, Entity], metaclass=ABCMeta):
    @abstractmethod
    def get(self) -> List[Entity]: ...

    @abstractmethod
    def get_by_id(self, id: UUID) -> List[Entity]: ...

    @abstractmethod
    def create(self, data: CreateDto): ...

    @abstractmethod
    def update(self, id: UUID, data: UpdateDto): ...

    @abstractmethod
    def delete(self, id: UUID): ...
