from typing import TypedDict


class CloudinaryConfig(TypedDict):
    cloud_name: str
    api_key: str
    api_secret: str
    env_variable: str


class Config(TypedDict):
    auth_api: str
    core_api: str
    checkout_base_url: str
    notification_api: str
    cloudinary: CloudinaryConfig
