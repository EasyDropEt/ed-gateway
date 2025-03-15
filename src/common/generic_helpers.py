import os
import uuid

from dotenv import load_dotenv

from src.common.typing.config import Config


def get_config() -> Config:
    load_dotenv()

    return {
        "auth_api": os.getenv("AUTH_API") or "",
        "core_api": os.getenv("CORE_API") or "",
    }

def get_new_id():
    return str(uuid.uuid4())
