import os
import uuid

from dotenv import load_dotenv

from ed_gateway.common.typing.config import Config


def get_config() -> Config:
    load_dotenv()

    return {
        "auth_api": _get_env_variable("AUTH_API"),
        "core_api": _get_env_variable("CORE_API"),
        "checkout_base_url": _get_env_variable("CHECKOUT_BASE_URL"),
        "notification_api": _get_env_variable("NOTIFICATION_API"),
        "cloudinary": {
            "cloud_name": _get_env_variable("CLOUDINARY_CLOUD_NAME"),
            "api_key": _get_env_variable("CLOUDINARY_API_KEY"),
            "api_secret": _get_env_variable("CLOUDINARY_API_SECRET"),
            "env_variable": _get_env_variable("CLOUDINARY_ENVIRONMENT_VARIABLE_NAME"),
        },
    }


def get_new_id():
    return str(uuid.uuid4())


def _get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable '{name}' is not set.")

    if not isinstance(value, str):
        raise TypeError(f"Environment variable '{name}' must be a string.")

    value = value.strip()
    if not value:
        raise ValueError(f"Environment variable '{name}' cannot be empty.")

    return value
