from typing import Generic, TypedDict, TypeVar

DataType = TypeVar("DataType")


class ApiResponse(Generic[DataType], TypedDict):
    is_success: bool
    message: str
    data: DataType
    errors: list[str]
