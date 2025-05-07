from abc import ABCMeta, abstractmethod
from typing import TypedDict


class InputImage:
    def __init__(self, file: object) -> None:
        self._file = file

    @property
    def file(self):
        return self._file


class UploadedImage(TypedDict):
    url: str
    secure_url: str


class ABCImageUploader(metaclass=ABCMeta):
    @abstractmethod
    async def upload(self, file: InputImage) -> UploadedImage: ...
