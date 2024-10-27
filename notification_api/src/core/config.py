from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    project_name: str = Field("notification_api", alias="PROJECT_NAME")
    broker_url: str = Field("amqp://user:password@rabbitmq:5672/", alias="BROKER_URL")


settings = Settings()
