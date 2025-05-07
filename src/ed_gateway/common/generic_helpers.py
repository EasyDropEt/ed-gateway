import os
import uuid

from dotenv import load_dotenv

from ed_gateway.common.typing.config import Config


def get_config() -> Config:
    load_dotenv()

    return {
        "auth_api": os.getenv("AUTH_API") or "",
        "core_api": os.getenv("CORE_API") or "",
        "cloudinary": {
            "cloud_name": os.getenv("CLOUDINARY_CLOUD_NAME") or "",
            "api_key": os.getenv("CLOUDINARY_API_KEY") or "",
            "api_secret": os.getenv("CLOUDINARY_API_SECRET") or "",
            "env_variable": os.getenv("CLOUDINARY_ENV_VARIABLE") or "",
        },
    }


def get_new_id():
    return str(uuid.uuid4())
