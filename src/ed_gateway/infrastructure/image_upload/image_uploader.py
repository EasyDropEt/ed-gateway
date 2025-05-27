import cloudinary
import cloudinary.uploader

from ed_gateway.application.contracts.infrastructure.image_upload.abc_image_uploader import (
    ABCImageUploader, InputImage, UploadedImage)
from ed_gateway.common.typing.config import CloudinaryConfig


class ImageUploader(ABCImageUploader):
    def __init__(self, config: CloudinaryConfig) -> None:
        cloudinary.config(
            cloud_name=config["cloud_name"],
            api_key=config["api_key"],
            api_secret=config["api_secret"],
            secure=True,
        )

    async def upload(self, file: InputImage) -> UploadedImage:
        return cloudinary.uploader.upload(file.file)
