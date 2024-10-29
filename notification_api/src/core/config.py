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
    postgres_url: str = Field(
        "postgresql+asyncpg://postgres:postgres@db:5432/foo", alias="POSTGRES_URL"
    )
    engine_echo: bool = Field(default=False, alias="ENGINE_ECHO")


settings = Settings()
