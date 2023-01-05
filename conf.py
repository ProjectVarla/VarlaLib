from typing import Optional
from pydantic import BaseSettings, validator
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):

    APP_NAME: str = "Varla-CLI"
    APP_TYPE: str = "Interface"

    GATEWAY_URL: Optional[str]

    NOTIFICATION_CORE_URL: Optional[str]
    DEFAULT_CHANNEL: Optional[str]

    @validator("NOTIFICATION_CORE_URL", always=True)
    def notification_core_url_validator(cls, v, values):
        return v if v else values["GATEWAY_URL"]


settings = Settings()
